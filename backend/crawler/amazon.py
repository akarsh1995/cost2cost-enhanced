import asyncio
import csv
import logging
from dataclasses import asdict, dataclass
from random import choice, random
from typing import List
from urllib.parse import urlencode

from aiohttp import ClientSession
from aiohttp.hdrs import USER_AGENT
from aiohttp.typedefs import PathLike
from crawler import create_new_session, fetch, user_agents
from lxml import html
from tqdm.asyncio import tqdm_asyncio

# todo differentiate between amazon search link vs actual product link

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers",
}

REGION = "in-en"


def create_duck_url(query: str, region="in-en"):
    params = urlencode(dict(kl=region, kp=-1, q=query.strip()))
    return f"https://html.duckduckgo.com/html?{params}"


DDG_RESULT_ROOT_XPATH = '//h2[contains(@class, "result")]//a'


MULTIPLE_PRODUCTS_XPATH = {
    "root": '//div[@data-asin]//div[contains(@cel_widget_id, "MAIN-SEARCH_RESULTS")]',
    "children": {
        "title": 'span[contains(@class, "a-size-medium")]/text()',
        "price": 'span[@class="a-price"]//text()',
    },
}


def get_mul_prod_paage_first_elem_dict_from_xpath(root_elem: html.HtmlElement):
    products = root_elem.xpath(MULTIPLE_PRODUCTS_XPATH["root"])
    return {
        child: products[0].xpath(f".//{xpath}")[0]
        for child, xpath in MULTIPLE_PRODUCTS_XPATH["children"].items()
    }


def is_multiple_products_page(html_elem: html.HtmlElement):
    return len(html_elem.xpath(MULTIPLE_PRODUCTS_XPATH["root"])) > 1


@dataclass
class DDGResult:
    title: str
    href: str


async def get_duck_duck_go_results(
    query: str, session: ClientSession, tries=0, max_tries=-1
) -> List[DDGResult]:
    url = create_duck_url("amazon.in " + query)
    response = await session.post(
        url, headers=headers | {USER_AGENT: choice(user_agents)["ua"]}
    )
    response = {"status": response.status, "text": await response.text()}
    if response["status"] == 200:
        root_elem = html.fromstring(response["text"])
        elems = root_elem.xpath(DDG_RESULT_ROOT_XPATH)
        results = []
        if elems:
            for elem in elems:
                result_url = elem.xpath("./@href")[0]
                result_title = elem.xpath("./text()")[0]
                results.append(DDGResult(result_title, result_url))
        else:
            logging.warning(f"No results found for the query: {query}")
        return results
    else:
        logging.warning(
            f"Encountered http response error: {response['status']} retrying {tries}th time"
        )
        await asyncio.sleep(
            2**tries + random() * 5
        )  # 5 - 10 seconds delay in case of limit reached
        if tries < max_tries or max_tries == -1:
            return await get_duck_duck_go_results(query, session, tries + 1, max_tries)
        else:
            logging.warning(f"Reached out max tries: {max_tries} for query: {query}")
            return []


AMAZON_PRICE_XPATH = (
    '//div[contains(@id, "apex_desktop")]//span[@class="a-price-whole"]/text()'
)


@dataclass
class AmazonProduct:
    title: str
    price: str = ""
    url: str = ""
    image_url: str = ""


async def fetch_result_from_amazon(
    title: str, first_result: str, session: ClientSession, tries: int = 0, max_tries=-1
) -> AmazonProduct:
    amazon_wp = await fetch(session, first_result, headers=headers)
    if amazon_wp["status"] == 200:
        root_elem = html.fromstring(amazon_wp["text"])
        page_has_multiple_prods = is_multiple_products_page(root_elem)

        price = ""
        amazon_title = ""
        if page_has_multiple_prods:
            logging.info(
                f"Is multiple products page taking first elem for link: {first_result}"
            )
            mul_dict = get_mul_prod_paage_first_elem_dict_from_xpath(root_elem)
            amazon_title = mul_dict["title"]
            price = mul_dict["price"]
        else:
            # single description page
            price_elems = root_elem.xpath(
                '//div[contains(@id, "apex_desktop")]//span[@class="a-price-whole"]/text()'
            )
            if price_elems:
                price = price_elems[0]
                amazon_title = root_elem.xpath(
                    '//h1[contains(@id, "title")]//span[contains(@id, "productTitle")]/text()'
                )
                if amazon_title:
                    amazon_title = amazon_title[0]
                else:
                    logging.warning(
                        f"Title on amazon detail page not found for title: {title}, url: {first_result}"
                    )
            else:
                logging.warning(
                    f"price element not found for title: {title}, link: {first_result}, xpath: {AMAZON_PRICE_XPATH}"
                )
        image_url = ""
        image_srcs = root_elem.xpath('//img[contains(@id, "landingImage")]/@src')
        if image_srcs:
            image_url = image_srcs[0]
        return AmazonProduct(
            title=title, price=price, url=first_result, image_url=image_url
        )
    else:
        await asyncio.sleep(
            2**tries + random() * 5
        )  # 5 - 10 seconds delay in case of limit reached
        if tries < max_tries or max_tries == -1:
            logging.warning(
                f"could not fetch the product from amazon for title: {title}, link: {first_result} retrying {tries + 1}th time"
            )
            return await fetch_result_from_amazon(
                title, first_result, session, tries + 1, max_tries
            )
        else:
            logging.warning(
                f"Reached maximum number of tries for title: {title}, link: {first_result}",
            )
            return AmazonProduct(title=title)


async def get_product_price_from_duck_then_amazon_amazon(
    title: str, session: ClientSession
) -> AmazonProduct:
    duck_results = await get_duck_duck_go_results(title, session)
    if duck_results:
        filtered_amazon_india_results = [
            r for r in duck_results if "amazon.in" in r.href
        ]

        if filtered_amazon_india_results:
            first_result = filtered_amazon_india_results[0].href
            return await fetch_result_from_amazon(title, first_result, session)
        else:
            logging.warning(
                f"Even though results are found on ddg but no amazon.in results found for {title} on duckduckgo"
            )
    else:
        logging.warning(f"no results found for {title} on duckduckgo")
    return AmazonProduct(title=title)


def write_to_csv(path: PathLike, to_csv=True):
    def decor(func):
        async def wrapper(*args, **kwargs):
            results = await func(*args, **kwargs)
            product_as_dict = asdict(results)
            if to_csv:
                with open(path, "a") as f:
                    writer = csv.DictWriter(
                        f, fieldnames=list(AmazonProduct.__annotations__.keys())
                    )
                    writer.writerows([product_as_dict])
            else:
                logging.info(str(product_as_dict))
            return results

        return wrapper

    return decor


# @write_to_csv("./amazon_prods.csv", True)
async def custom_fetch(title, session):
    await asyncio.sleep((30 + random() * 60) if random() > 0.5 else random() * 30)
    return await get_product_price_from_duck_then_amazon_amazon(title, session)


async def main(loop, titles: List[str]):
    async with create_new_session(loop) as s:
        s = await tqdm_asyncio.gather(*[custom_fetch(t, s) for t in titles])


if __name__ == "__main__":
    import json

    with open("/home/akarshj/Programming/pdf_read_py/backend/cpus.json") as cpu_file:
        titles: List[str] = json.load(cpu_file)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(loop, titles))
