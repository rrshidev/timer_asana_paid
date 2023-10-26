import asyncio
from time import perf_counter

from app.celery_config import celery_app
from app.services import RedisStorage
from app.logger import logger
from bot import markups
from bot.utils import get_redis_entry, get_time_str
from bot.const import phrases
from bot.const import enums


async def tick(user_id: id) -> None:
    from bot import bot_instance

    user_entry = get_redis_entry(
        user_id=user_id,
        practice=enums.Practices.MEDITATION.value,
    )

    logger.info(f"ENTRY {user_entry}")

    while True:
        start_time = perf_counter()
        user_timer_data = RedisStorage.hgetall(
            database=3,
            name=user_entry,
        )

        logger.info(f"DATA {user_timer_data}")

        timer_paused: bool = bool(int(user_timer_data.get("timer_paused")))
        if timer_paused:
            break

        total_sec: int = int(user_timer_data.get("total_sec"))
        rest_sec: int = int(user_timer_data.get("rest_sec"))

        message_id: int = int(user_timer_data.get("message_id"))

        logger.info(f"TOTAL {total_sec} {rest_sec}")

        # descrease seconds
        if rest_sec > 0:
            rest_sec -= 1

        await bot_instance.edit_message_text(
            chat_id=user_id,
            message_id=message_id,
            text=phrases.phrase_for_timer_message(
                total=get_time_str(seconds=total_sec),
                rest=get_time_str(seconds=rest_sec),
                status=True,
            ),
            reply_markup=markups.practice_stop_process_markup(),
        )

        RedisStorage.hset(
            database=3,
            name=user_entry,
            mapping=dict(
                rest_sec=rest_sec,
            ),
        )

        if rest_sec == 0:
            await bot_instance.send_message(
                chat_id=user_id,
                text="Практика окончена!",
                reply_markup=markups.step_back_markup(),
            )
            break

        end_time = perf_counter()
        await asyncio.sleep(max(1 - (end_time - start_time), 0))


@celery_app.task()
def timer(user_id: int) -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tick(user_id=user_id))
