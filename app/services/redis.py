from typing import Any
import aioredis


class RedisConnector:
    def __init__(self, url: str):
        self.connection = aioredis.from_url(url=url)

    async def get(self, name: str) -> str:
        return await self.connection.get(name=name)

    async def set(self, name: str, value: Any) -> None:
        return await self.connection.set(name=name, value=value)

