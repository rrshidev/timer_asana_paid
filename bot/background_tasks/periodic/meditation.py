import asyncio

from aiogram.types import Message

from app.celery_config import celery_app
from app.services import rc
from app.logger import logger
from bot import markups
from bot.routers.meditation_practice import timer_message
from bot.services import timer_service


async def tick(entry_name: str) -> None:
    logger.info(f"{entry_name} - TICK")
    total_time = int(rc.get(f"{entry_name}_total"))
    rest_time = int(rc.get(f"{entry_name}_rest"))

    mins, secs = divmod(rest_time, 60)
    timer_value = '{:02d}:{:02d}'.format(mins, secs)

    message: Message = timer_service.get_entry(entry_name=entry_name).get("message")
    if not message:
        return

    await message.edit_text(
        text=timer_message(
            total=total_time, 
            rest=timer_value, 
            status=True,
        ),
        reply_markup=markups.practice_stop_process(),
    )

    rc.set(
        name=f"{entry_name}_rest",
        value=rest_time-1,    
    )
    if rest_time == 0:
        await message.reply(
            text="Практика окончена!",
            reply_markup=markups.step_back_markup(),
        )
        timer_service.remove_entry(entry_name=entry_name)


@celery_app.task()
def timer(entry_name: str) -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        tick(
            entry_name=entry_name,
        )
    )
