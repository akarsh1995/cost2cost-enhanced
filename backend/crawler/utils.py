import asyncio
import logging
from random import random
from typing import List

from lxml.html import HtmlElement


def parse_all_text_from_xpath_return(elems: List[HtmlElement]) -> str:
    text_list = [" ".join(map(lambda x: x.strip(), elem.itertext())) for elem in elems]
    if elems:
        return " ".join(text_list)
    else:
        return ""


from crawler import fetch, post


class RetryRequest:
    request_name: str

    def __init__(self) -> None:
        self._current_try = 1

    async def _request(
        self, url: str, headers: dict = {}, max_tries: int = 100, is_get=True
    ) -> str:
        response = (
            await fetch(url, headers=headers)
            if is_get
            else await post(url, headers=headers)
        )
        if response.ok:
            return await response.text()
        elif self._current_try < max_tries:
            # in case of hitting the limit we'll attempt again after exponential wait time
            logging.warning(
                f"Received response status {response.status} for request "
                "{self.request_name}. Retrying {self._current_try + 1} time."
            )
            await asyncio.sleep(2**self._current_try + random() * 5)
            self._current_try += 1
            return await self._request(
                url,
                headers,
                max_tries=max_tries,
                is_get=is_get,
            )
        else:
            return ""

    async def get(self, url: str, headers: dict = {}, max_tries: int = 100):
        response = await self._request(url, headers, max_tries)
        return response

    async def post(self, url: str, headers: dict = {}, max_tries: int = 100):
        return await self._request(url, headers, max_tries)


if __name__ == "__main__":

    async def main():
        async with client as _:
            r = RetryRequest()
            res = await r.get("https://jsonplaceholder.typicode.com/todos/1")
            print(res)

    from crawler import client, loop

    loop.run_until_complete(main())
