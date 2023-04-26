import asyncio
from functools import reduce
from random import random
from typing import Dict, Iterable, List, TypedDict

from aiohttp import ClientSession
from aiohttp.typedefs import PathLike
from crawler import create_new_session, fetch, fetch_all
from functions_framework import json
from lxml import html
from tqdm.asyncio import tqdm_asyncio


class ProductType(TypedDict):
    title: str
    price: str
    url: str
    image_url: str


async def get_all_products_from_page(
    page_link: str, session: ClientSession
) -> List[ProductType]:
    await asyncio.sleep(random() * 2)
    source_ = await fetch(session=session, url=page_link)
    landing_page_html = html.fromstring(source_["text"])
    titles = landing_page_html.xpath('//div[@class="product-layout "]//h4/a/text()')
    links = landing_page_html.xpath('//div[@class="product-layout "]//h4/a/@href')
    prices = landing_page_html.xpath(
        '//div[@class="product-layout "]//span[@class="price-new"]/text()'
    )
    images = landing_page_html.xpath(
        '//div[@class="product-layout "]//img[contains(@data-src, "180x180")]/@data-src'
    )

    assert len(titles) == len(links) == len(prices) == len(images)
    return [
        {"title": t, "url": l, "price": p, "image_url": "https:" + i}
        for t, l, p, i in zip(titles, links, prices, images)
    ]


class CategoryLinkType(TypedDict):
    category: str
    url: str


async def get_page_links_from_categories(
    category_links: Iterable[CategoryLinkType], session: ClientSession
) -> Dict[str, Iterable[str]]:
    cat_landing_sources = await fetch_all(
        map(lambda c: c["url"], category_links), "fetch_page_information", session
    )

    cat_n_pages = []
    for source in cat_landing_sources:
        landing_page_html = html.fromstring(source["text"])
        page_string: str = landing_page_html.xpath(
            '//div[contains(@class, "product-filter-bottom")]//div[contains(@class, "text-right")]/text()'
        )[0]
        start = page_string.find("(")
        end = page_string.find(")")
        string_n = (
            page_string[start + 1 : end].replace("Page", "").replace("s", "").strip()
        )
        cat_n_pages.append(int(string_n))

    cat_prod_map = {}
    for c, cat_n_page in zip(category_links, cat_n_pages):
        cat_all_page_link = map(
            lambda page_num: c["url"] + f"?page={page_num}",
            range(1, cat_n_page + 1),
        )
        cat_prod_map[c["category"]] = list(cat_all_page_link)
    return cat_prod_map


async def get_all_products_for_category(
    category: str, link_iterator: Iterable[str], session: ClientSession
):
    products = await tqdm_asyncio.gather(
        *[get_all_products_from_page(l, session) for l in link_iterator],
        desc="category {}".format(category),
    )
    x = reduce(lambda pl1, pl2: pl1 + pl2, products)
    return {"category": category, "products": x}


async def get_categories_from_landing_page(
    session: ClientSession,
) -> List[CategoryLinkType]:
    response = await fetch(session, "https://mdcomputers.in")
    html_page = html.fromstring(response["text"])
    category_base_path = '//li[contains(@class, "vertical")]/a[@class="clearfix"]'
    category_heading_path = ".//span//strong/text()"
    category_url_path = "./@href"
    category_page_links: List[CategoryLinkType] = [
        {
            "category": elem.xpath(category_heading_path)[0],
            "url": elem.xpath(category_url_path)[0],
        }
        for elem in html_page.xpath(category_base_path)
    ]
    return category_page_links


async def get_all_products_from_all_categories(
    cat_prod_page_map: Dict[str, Iterable[str]],
    session: ClientSession,
):
    cat_pro = await asyncio.gather(
        *[
            get_all_products_for_category(ct, li, session)
            for ct, li in cat_prod_page_map.items()
        ]
    )
    return cat_pro


async def crawl(loop: asyncio.AbstractEventLoop, json_path: PathLike):
    async with create_new_session(loop) as sess:
        category_page_links = await get_categories_from_landing_page(sess)
        cat_prod_page_map = await get_page_links_from_categories(
            category_page_links[:1], sess
        )
        all_products = await get_all_products_from_all_categories(
            cat_prod_page_map, sess
        )

        with open(json_path, "w") as f:
            json.dump(all_products, f)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(crawl(loop, "./all_prods_md_comp.json"))
