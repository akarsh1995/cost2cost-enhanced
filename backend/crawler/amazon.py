import logging
from dataclasses import dataclass, field
from typing import Dict, List

from crawler import loop, user_agents
from crawler.duckduckgo import DuckDuckGo
from crawler.utils import RetryRequest, parse_all_text_from_xpath_return
from lxml import html

# todo differentiate between amazon search link vs actual product link

HEADERS = {
    "User-Agent": user_agents[0]["ua"],
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

XPATHS = {
    "PRODUCT_DESCRIPTION_PAGE": {
        "CENTER_DIV": {
            "root": '//div[@id = "centerCol"]',
            "children": {
                "title": 'span[contains(@id, "productTitle")]',
                "price": 'span[@class="a-price-whole"]',
            },
        },
        "LEFT_IMAGE_DIV": {
            "root": '//img[contains(@id, "landingImage")]',
        },
    },
    "MULTIPLE_PRODUCTS": {
        "PRODUCT_LIST_DIV": {
            "root": '//div[@data-asin]//div[contains(@cel_widget_id, "MAIN-SEARCH_RESULTS")]',
            "children": {
                "title": 'span[contains(@class, "a-size-medium")]',
                "price": 'span[@class="a-price"]',
                "image": 'img[@class="s-image"]',
            },
        },
    },
}


@dataclass
class ProductDetailPage:
    root_elem: html.HtmlElement
    xpath = XPATHS["PRODUCT_DESCRIPTION_PAGE"]["CENTER_DIV"]["children"]
    image_xpath = XPATHS["PRODUCT_DESCRIPTION_PAGE"]["LEFT_IMAGE_DIV"]["root"]

    def get_product(self):
        return {
            "title": self.get_title(),
            "price": self.get_price(),
            "image": self.get_image(),
        }

    def get_title(self) -> str:
        return parse_all_text_from_xpath_return(
            self.root_elem.xpath(f".//{self.xpath['title']}")
        ).strip()

    def get_price(self) -> str:
        return parse_all_text_from_xpath_return(
            self.root_elem.xpath(f".//{self.xpath['price']}")
        ).strip()

    def get_image(self) -> str:
        images = self.root_elem.xpath(self.image_xpath)
        if images:
            return images[0].get("src")
        return ""


@dataclass
class MultipleProductPage:
    product_elems: List[html.HtmlElement]
    xpath = XPATHS["MULTIPLE_PRODUCTS"]["PRODUCT_LIST_DIV"]["children"]

    def get_products(self) -> List[Dict[str, str]]:
        l = []
        for product_section in self.product_elems:
            title = parse_all_text_from_xpath_return(
                product_section.xpath(f".//{self.xpath['title']}")
            ).strip()
            price = parse_all_text_from_xpath_return(
                product_section.xpath(f".//{self.xpath['price']}")
            ).strip()
            __import__("pdb").set_trace()

            image = ""
            images = product_section.xpath(f".//{self.xpath['image']}")
            if images:
                image = images[0].get("src")
            l.append(
                {
                    "title": title,
                    "price": price,
                    "image": image,
                }
            )
        return l


@dataclass
class AmazonCrawl(RetryRequest):
    root_elem: html.HtmlElement = field(init=False)
    product_link: str = field(default="", init=False)
    request_name = "amazon crawl"

    async def crawl_using_ddg(self, category, vendor, product, **kwargs):
        ddg_query = DuckDuckGo(
            f"{category} {vendor} {product}", filter_domain="amazon.in", **kwargs
        )
        results = await ddg_query.search(kwargs["headers"])
        if results:
            self.product_link = results[0].href
        return await self.fetch_html_page(self.product_link)

    async def fetch_html_page(self, product_link: str):
        response_text = await self.get(product_link, headers=HEADERS)
        if response_text:
            self.root_elem = html.fromstring(response_text)
        return self.get_product_details()

    def get_product_details(self) -> Dict[str, str]:
        if self._is_multiple_product_search_page():
            mul_prods = self.get_products_from_multiple_products_page()
            first_prod = mul_prods.get_products()
            single_prod = first_prod[0]
        else:
            single_prod = self.get_product_from_detail_page().get_product()
        return single_prod

    def _is_multiple_product_search_page(self):
        return len(self._get_multiple_products()) > 1

    def _get_multiple_products(self) -> List[html.HtmlElement]:
        return self.root_elem.xpath(
            XPATHS["MULTIPLE_PRODUCTS"]["PRODUCT_LIST_DIV"]["root"]
        )

    def get_products_from_multiple_products_page(self) -> MultipleProductPage:
        return MultipleProductPage(self._get_multiple_products())

    def get_product_from_detail_page(self) -> ProductDetailPage:
        product_detail_page = self.root_elem.xpath(
            XPATHS["PRODUCT_DESCRIPTION_PAGE"]["CENTER_DIV"]["root"]
        )
        if not product_detail_page:
            logging.warning(
                f"Looks like this link is not a product detail page. link: {self.product_link}"
            )
        return ProductDetailPage(product_detail_page[0])


# @dataclass
# class AmazonProduct:
#     title: str
#     price: int = 0
#     url: str = ""
#     image_url: str = ""
#     vendor: str = "amazon"
#     category: str = "cpu"
#     timestamp: datetime = field(default_factory=datetime.now)

#     @staticmethod
#     def clean_price(price):
#         if price:
#             return int(price.replace(",", "").replace("₹", "").strip())
#         return 0


# def write_to(to="db", path: PathLike = "amazon_prods.csv"):
#     if not Product.table_exists():
#         Product.create_table()

#     def decor(func):
#         async def wrapper(*args, **kwargs):
#             results = await func(*args, **kwargs)
#             product_as_dict = asdict(results)
#             if to == "csv":
#                 with open(path, "a") as f:
#                     writer = csv.DictWriter(
#                         f, fieldnames=list(AmazonProduct.__annotations__.keys())
#                     )
#                     writer.writerows([product_as_dict])
#             elif to == "db":
#                 Product.create(**product_as_dict)
#             return results

#         return wrapper

#     return decor


# @write_to(to="db")
# async def custom_fetch(title, session):
#     await asyncio.sleep(random() * 200)
#     return await get_product_price_from_duck_then_amazon_amazon(title, session)


# async def main(loop, titles: List[str]):
#     async with create_new_session(loop) as s:
#         s = await tqdm_asyncio.gather(*[custom_fetch(t, s) for t in titles])


if __name__ == "__main__":
    import json

    ac = AmazonCrawl()
    # res = loop.run_until_complete(ac.crawl_using_ddg("cpu", "intel", "i5-11400"))
    res = loop.run_until_complete(
        ac.fetch_html_page(
            "https://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=i5"
        )
    )
    print(res)
