import asyncio
from time import perf_counter

from app.celery_config import celery_app
from app.services import RedisStorage
from app.logger import logger
from bot.const import phrases, enums


async def tick(user_id: id) -> None:
    from bot import bot_instance

    user_entry = get_redis_entry(
        user_id=user_id,
        practice=enums.Practices.PRANAYAMA.value,
    )

    while True:
        start_time = perf_counter()
        user_timer_data = RedisStorage.hgerall(
            database=3,
            name=user_entry,
        )

        total_sec: int = int(user_timer_data.get("total_sec"))
        rest_sec: int =  int(user_timer_data.get("rest_sec"))

        message_id: int = int(user_timer_data.get("messsage_id"))





@celery_app.task()
def timer(user_id: int) -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tick(user_id=user_id))
