from typing import Any

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ErrorEvent
from aiogram.fsm.storage.redis import RedisStorage

from .decorators import *
from app import logger
from app.settings import bot_settings, redis_settings
from .routers import commands_router, form_router, messages_router, choose_practice_router, choose_asana_practice_router, choose_pranayama_practice_router, choose_meditation_practice_router
from .middlewares import LoggingMiddleware


bot = Bot(token=bot_settings.TOKEN, parse_mode="html")
dp = Dispatcher(storage=RedisStorage.from_url(redis_settings.fsm_url))

# set middlewares
dp.message.outer_middleware(LoggingMiddleware())

# set routers
dp.include_router(form_router)
dp.include_router(commands_router)
dp.include_router(choose_practice_router)
dp.include_router(choose_asana_practice_router)
dp.include_router(choose_pranayama_practice_router)
dp.include_router(choose_meditation_practice_router)
dp.include_router(messages_router)

@dp.error(F.update.message.as_("message"))
async def error_handler(event: ErrorEvent, message: Message) -> Any:
    logger.critical(f"Critical error caused by {event.exception}", exc_info=True)
    await message.answer(
        text="Something went wrong, try again later",
    )
