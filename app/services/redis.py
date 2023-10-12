from typing import Any
import redis


class RedisConnector:
    def __init__(self, url: str):
        self.connection = redis.from_url(url=url)

    def get(self, name: str) -> str:
        return self.connection.get(name=name)

    def set(self, name: str, value: Any) -> None:
        return self.connection.set(name=name, value=value)
