from typing import Any
import redis


class RedisConnector:
    @staticmethod
    def get(database: str, name: str) -> str:
        return redis.from_url(url=database).get(name=name)

    @staticmethod
    def set(database: str, name: str, value: Any) -> None:
        return redis.from_url(url=database).set(name=name, value=value)
