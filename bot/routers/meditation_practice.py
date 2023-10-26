from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from celery.result import AsyncResult

from app.logger import logger
from app.services import RedisStorage
import bot.const.phrases as phrases
from bot import markups
from bot.background_tasks import meditation_timer_task
from bot.utils import get_redis_entry, str_to_time, get_time_str
from bot.filters import ButtonFilter
from bot.buttons import (
    ChoosePracticeButtons,
)
from bot.callbacks import PracticeTimerCallback
from bot.const import enums


choose_meditation_practice_router = Router()


class Meditation(StatesGroup):
    time = State()
    running = State()


@choose_meditation_practice_router.message(
    ButtonFilter(button=ChoosePracticeButtons.MEDITATION)
)
async def meditation_practice(message: Message, state: FSMContext) -> None:
    text = phrases.phrase_meditation()
    markup = markups.step_back_markup()

    await state.set_state(Meditation.time)
    await message.answer(
        text=text,
        reply_markup=markup,
    )


@choose_meditation_practice_router.message(Meditation.time, F.text.regexp(r"^\d+(:\d+)?$"))
async def enter_meditation_time(message: Message, state: FSMContext) -> None:
    total_time = str_to_time(input=message.text)

    sticker = FSInputFile("static/buddha_start_timer.webp")
    await message.answer_sticker(sticker)

    total_time_str = get_time_str(seconds=total_time.total_seconds())
    edit_message = await message.answer(
        text=phrases.phrase_for_timer_message(
            total=total_time_str,
            rest=total_time_str,
        ),
        reply_markup=markups.practice_stop_process_markup(),
    )

    RedisStorage.hset(
        database=3,
        name=get_redis_entry(
            user_id=message.from_user.id,
            practice=enums.Practices.MEDITATION.value,
        ),
        mapping=dict(
            total_sec=int(total_time.total_seconds()),
            rest_sec=int(total_time.total_seconds()),
            message_id=edit_message.message_id,
            timer_paused=0,
        ),
    )

    task: AsyncResult = meditation_timer_task.apply_async(
        args=[message.from_user.id],
        countdown=0,
    )
    edited = edit_message.edit_reply_markup(
        reply_markup=markups.practice_stop_process_markup(task_id=task.id),
    )
    logger.info(f"STATUS {edited}")

    await state.set_state(Meditation.running)


@choose_meditation_practice_router.message(Meditation.time, ~F.text.regexp(r"^\d+(:\d+)?$"))
async def wrong_meditation_time(message: Message, state: FSMContext) -> None:
    await message.answer(
        text="Wrong",
    )


@choose_meditation_practice_router.callback_query(
    Meditation.running, PracticeTimerCallback.filter(F.action == "pause")
)
async def pause_mediation(
    query: CallbackQuery,
    callback_data: PracticeTimerCallback,
    state: FSMContext,
    bot: Bot,
) -> None:
    logger.info(f"GOTCHA {callback_data} |")
    AsyncResult(callback_data.task_id).revoke()

    user_timer_data = RedisStorage.hgetall(
        database=3,
        name=get_redis_entry(
            user_id=query.from_user.id,
            practice=enums.Practices.MEDITATION.value,
        ),
    )

    message_id: int = user_timer_data.get("message_id")
    total_time_str = get_time_str(seconds=int(user_timer_data.get("total_sec")))

    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=message_id,
        text=phrases.phrase_for_timer_message(
            total=total_time_str,
            rest=total_time_str,
            status=False,
        ),
        reply_markup=markups.practice_continue_process_markup(),
    )

    await query.answer()


# @choose_meditation_practice_router.message(Meditation.time, ~F.text.isdigit())
# async def wrong_meditation_time(message: Message, state: FSMContext) -> None:
#     await message.answer(
#         text="Wrong",
#     )

# @choose_meditation_practice_router.message(Meditation.time, ~F.text.isdigit())
# async def wrong_meditation_time(message: Message, state: FSMContext) -> None:
#     await message.answer(
#         text="Wrong",
#     )
