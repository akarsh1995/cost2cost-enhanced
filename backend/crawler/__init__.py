# buy from the right online store and minimize the price
# tpstech has no restrictions
# mdcomputers has no restrictions
# vedanta has limit of 1200 requests / 5 min
# vedant computers 1200 requests per 5 min

import asyncio
import json
import os
from pathlib import Path
from random import choice
from typing import Iterable, List, Optional, TypedDict

import aiohttp
from aiohttp.hdrs import USER_AGENT
from tqdm.asyncio import tqdm_asyncio


class UserAgents(TypedDict):
    ua: str
    pct: float


user_agents: List[UserAgents] = json.loads(
    Path(os.environ["USER_AGENTS_JSON"]).read_text()
)


class RespType(TypedDict):
    status: int
    text: str


loop = asyncio.get_event_loop()

client = aiohttp.ClientSession(loop=loop)


async def fetch(url: str, headers: Optional[dict] = None) -> aiohttp.ClientResponse:
    custom_headers = {}
    custom_headers.update({USER_AGENT: choice(user_agents)["ua"]} | (headers or {}))
    return await client.get(url, headers=custom_headers)


async def post(url: str, headers: Optional[dict] = None) -> aiohttp.ClientResponse:
    custom_headers = {}
    custom_headers.update({USER_AGENT: choice(user_agents)["ua"]} | (headers or {}))
    return await client.post(url, headers=custom_headers)


async def fetch_all(
    urls: Iterable[str],
    description: str,
    headers: None,
) -> List[RespType]:
    results = await tqdm_asyncio.gather(
        *[fetch(url, headers) for url in urls], desc=description
    )
    return results


def create_new_session(loop: asyncio.AbstractEventLoop):
    return aiohttp.ClientSession(loop=loop)
