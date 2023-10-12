from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import asyncio
from asyncio import exceptions

from app.services import rc
import bot.const.phrases as phrases
from bot import markups
from bot.filters import ButtonFilter
from bot.buttons import ChoosePracticeButtons
from bot.const import const, enums
from bot.services import timer_service


choose_meditation_practice_router = Router()


class Meditation(StatesGroup):
    time = State()


def timer_message(total: int, rest: int = 0, status: bool = True):
    text = f'Идёт медитация\n\nВыбранное время: {total} минут'
    if rest:
        text += f'\n\nОставшееся время: {rest}'
    text += f'\n\nRunning' if status else f'\n\nPaused'

    return text


@choose_meditation_practice_router.message(ButtonFilter(button=ChoosePracticeButtons.MEDITATION))
async def meditation_practice(message: Message, state: FSMContext) -> None:
    text = phrases.phrase_meditation()
    markup = markups.step_back_markup()

    await state.set_state(Meditation.time)
    await message.answer(
        text=text,
        reply_markup=markup,
    )


@choose_meditation_practice_router.message(Meditation.time, F.text.isdigit())
async def enter_meditation_time(message: Message, state: FSMContext) -> None:
    const.timer_stopped = False
    const.timer_paused = False

    total_time = int(message.text) 
    total_time_seconds = total_time * 60
    entry_name = f'{message.from_user.id}_{enums.Practices.MEDITATION.value}'

    rc.set(name=f"{entry_name}_total", value=total_time_seconds)
    rc.set(name=f"{entry_name}_rest", value=total_time_seconds)

    sticker = FSInputFile("static/buddha_start_timer.webp")
    await message.answer_sticker(sticker)

    edit_message = await message.answer(
        text=timer_message(total=total_time),
        reply_markup=markups.practice_stop_process_markup(),
    )
    timer_service.set_entry(entry_name=entry_name, message=edit_message)

    await state.clear()


@choose_meditation_practice_router.message(Meditation.time, ~F.text.isdigit())
async def wrong_meditation_time(message: Message, state: FSMContext) -> None:
    
    await message.answer(
        text="Wrong",
    )



