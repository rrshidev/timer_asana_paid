import json
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from app import logger


class LoggingMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        pass

    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], message: Message, data: Dict[str, Any]) -> Any:
        logger.info("=============== INCOMING UPDATE ================")
        logger.info(json.dumps(dict(message), sort_keys=False, indent=4, default=str))
        logger.info("================================================")
        return await handler(message, data)


# class ThrottlingMiddleware(BaseMiddleware):
#     def __init__(self) -> None:
#         pass

#     async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], message: Message, data: Dict[str, Any]) -> Any:

#         return await handler(message, data)
