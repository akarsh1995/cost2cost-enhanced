import asyncio
import logging
from dataclasses import dataclass, field
from random import choice, random
from typing import List, Optional
from urllib.parse import urlencode

from aiohttp import ClientResponse, ClientSession
from aiohttp.hdrs import USER_AGENT
from crawler import client, loop, user_agents
from crawler.utils import RetryRequest, parse_all_text_from_xpath_return
from lxml import html

headers = {
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

DDG_RESULT_ROOT_XPATH = (
    '//div[contains(@class, "result results_links results_links_deep")]'
)


@dataclass
class DDGResult:
    title: str
    description: str
    href: str


@dataclass
class DuckDuckGo(RetryRequest):
    query: str
    filter_domain: str = "amazon.in"
    region: str = "in-en"
    max_retries: int = 100
    html_source: str = field(default="", init=False)
    root_elem: html.HtmlElement = field(init=False)
    request_name: str = field(default="Duck Duck Go", init=False)

    async def search(self, headers: Optional[dict] = None) -> List[DDGResult]:
        self.html_source = await self.post(
            self.create_url(),
            headers=(headers or {}) | {USER_AGENT: choice(user_agents)["ua"]},
            max_tries=self.max_retries,
        )
        if self.html_source:
            self.parse_response()
            ri = self.parse_ranked_items()
            return ri
        return []

    def parse_response(self):
        self.root_elem = html.fromstring(self.html_source)

    def create_url(self) -> str:
        if self.filter_domain:
            query = f"{self.filter_domain} {self.query.strip()}"
        else:
            query = self.query
        params = urlencode(dict(kl=self.region, kp=-1, q=query))
        return f"https://html.duckduckgo.com/html?{params}"

    def parse_ranked_items(self) -> List[DDGResult]:
        elems = self.root_elem.xpath(DDG_RESULT_ROOT_XPATH)
        results = []
        if elems:
            for elem in elems:
                result = self.parse_ddg_from_elem(elem)
                if result:
                    results.append(result)
        return results

    def parse_ddg_from_elem(self, elem: html.HtmlElement) -> Optional[DDGResult]:
        title = parse_all_text_from_xpath_return(elem.xpath(".//h2//a")).strip()
        url = parse_all_text_from_xpath_return(
            elem.xpath('.//a[contains(@class, "result__url")]')
        ).strip()
        if not url.startswith("https"):
            url = f"https://{url}"
        description = parse_all_text_from_xpath_return(
            elem.xpath('.//a[contains(@class, "result__snippet")]')
        ).strip()
        if self.filter_domain:
            if self.filter_domain in url:
                return DDGResult(title, description, url)


if __name__ == "__main__":

    async def main():
        async with client as _:
            d = DuckDuckGo("i5-10400")
            results = await d.search()
            __import__("pprint").pprint(results)

    loop.run_until_complete(main())
