from typing import Any, Dict
from redis import Redis


class RedisStorage:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.connections = {}

    def __connect_to_database__(self, database: int) -> Redis:
        if database not in self.connections:
            self.connections[database] = Redis(
                host=self.host, port=self.port, decode_responses=True
            )
        return self.connections[database]

    def get(self, database: int, name: str) -> str:
        return self.__connect_to_database__(database=database).get(name=name)

    def set(self, database: int, name: str, value: Any) -> bool:
        return self.__connect_to_database__(database=database).set(
            name=name, value=value
        )

    def hset(self, database: int, name: str, mapping: Dict) -> bool:
        return self.__connect_to_database__(database=database).hset(
            name=name, mapping=mapping
        )

    def hgetall(self, database: int, name: str) -> Dict:
        return self.__connect_to_database__(database=database).hgetall(name=name)
