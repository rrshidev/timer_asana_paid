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
from bot.buttons import ChoosePracticeButtons
from bot.callbacks import PracticeTimerCallback
from bot.const import enums


choose_meditation_practice_router = Router()


class Meditation(StatesGroup):
    time = State()
    running = State()


@choose_meditation_practice_router.message(ButtonFilter(button=ChoosePracticeButtons.MEDITATION))
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
            status=enums.TimerStatus.RUNNING
        ),
        reply_markup=markups.practice_stop_process_markup(),
    )

    user_entry = get_redis_entry(
        user_id=message.from_user.id,
        practice=enums.Practices.MEDITATION.value,
    )

    RedisStorage.hset(
        database=3,
        name=user_entry,
        mapping=dict(
            total_sec=int(total_time.total_seconds()),
            rest_sec=int(total_time.total_seconds()),
            message_id=edit_message.message_id,
        ),
    )

    task: AsyncResult = meditation_timer_task.apply_async(
        args=[message.from_user.id],
        countdown=0,
    )

    RedisStorage.hset(
        database=3,
        name=user_entry,
        mapping=dict(
            task_id=task.id,
        ),
    )

    await state.set_state(Meditation.running)


@choose_meditation_practice_router.message(
    Meditation.time, ~F.text.regexp(r"^\d+(:\d+)?$")
)
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
    user_timer_data = RedisStorage.hgetall(
        database=3,
        name=get_redis_entry(
            user_id=query.from_user.id,
            practice=enums.Practices.MEDITATION.value,
        ),
    )

    AsyncResult(user_timer_data.get("task_id")).revoke(terminate=True)
    message_id: int = user_timer_data.get("message_id")
    total_time_str = get_time_str(seconds=int(user_timer_data.get("total_sec")))
    rest_time_str = get_time_str(seconds=int(user_timer_data.get("rest_sec")))

    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=message_id,
        text=phrases.phrase_for_timer_message(
            total=total_time_str,
            rest=rest_time_str,
            status=enums.TimerStatus.PAUSED,
        ),
        reply_markup=markups.practice_continue_process_markup(),
    )

    await query.answer()


@choose_meditation_practice_router.callback_query(
    Meditation.running, PracticeTimerCallback.filter(F.action == "stop")
)
async def stop_mediation(
    query: CallbackQuery,
    callback_data: PracticeTimerCallback,
    state: FSMContext,
    bot: Bot,
) -> None:
    user_entry = get_redis_entry(
        user_id=query.from_user.id,
        practice=enums.Practices.MEDITATION.value,
    )
    user_timer_data = RedisStorage.hgetall(
        database=3,
        name=user_entry,
    )

    AsyncResult(user_timer_data.get("task_id")).revoke(terminate=True)
    message_id: int = user_timer_data.get("message_id")
    total_time_str = get_time_str(seconds=int(user_timer_data.get("total_sec")))
    rest_time_str = get_time_str(seconds=int(user_timer_data.get("rest_sec")))

    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=message_id,
        text=phrases.phrase_for_timer_message(
            total=total_time_str,
            rest=rest_time_str,
            status=enums.TimerStatus.STOPPED,
        ),
        reply_markup=None,
    )
    await bot.send_message(
        chat_id=query.from_user.id,
        text="Практика окончена!",
        reply_markup=markups.choose_practice_markup(),
    )

    RedisStorage.hset(
        database=3,
        name=user_entry,
        mapping=dict(
            total_sec=0,
            rest_sec=0,
        ),
    )

    await query.answer()


@choose_meditation_practice_router.callback_query(
    Meditation.running, 
    PracticeTimerCallback.filter(F.action == "resume")
)
async def resume_mediation(
    query: CallbackQuery,
    callback_data: PracticeTimerCallback,
    state: FSMContext,
    bot: Bot,
) -> None:
    user_entry = get_redis_entry(
        user_id=query.from_user.id,
        practice=enums.Practices.MEDITATION.value,
    )
    user_timer_data = RedisStorage.hgetall(
        database=3,
        name=user_entry,
    )

    message_id: int = user_timer_data.get("message_id")
    total_time_str = get_time_str(seconds=int(user_timer_data.get("total_sec")))
    rest_time_str = get_time_str(seconds=int(user_timer_data.get("rest_sec")))

    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=message_id,
        text=phrases.phrase_for_timer_message(
            total=total_time_str, rest=rest_time_str, status=enums.TimerStatus.RUNNING
        ),
        reply_markup=markups.practice_stop_process_markup(),
    )

    task: AsyncResult = meditation_timer_task.apply_async(
        args=[query.from_user.id],
        countdown=0,
    )

    RedisStorage.hset(
        database=3,
        name=user_entry,
        mapping=dict(
            task_id=task.id,
        ),
    )

    await query.answer()
