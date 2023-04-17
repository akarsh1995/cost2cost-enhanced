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


async def fetch(
    session: aiohttp.ClientSession, url: str, headers: Optional[dict] = None
) -> RespType:
    session.headers.add(USER_AGENT, choice(user_agents)["ua"])
    session.headers.update(headers or {})
    async with session.get(url) as response:
        return {"status": response.status, "text": await response.text()}


async def fetch_all(
    urls: Iterable[str], description: str, session: aiohttp.ClientSession
) -> List[RespType]:
    results = await tqdm_asyncio.gather(
        *[fetch(session, url) for url in urls], desc=description
    )
    return results


def create_new_session(loop: asyncio.AbstractEventLoop):
    return aiohttp.ClientSession(loop=loop)
