from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import bot.const.phrases as phrases
from bot import markups
from bot.filters import ButtonFilter
from bot.buttons import ChoosePracticeButtons


choose_meditation_practice_router = Router()


class Meditation(StatesGroup):
    time = State()


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
    minutes = message.text
    await state.clear()
    
    await message.answer(
        text="Right",
    )


@choose_meditation_practice_router.message(Meditation.time, ~F.text.isdigit())
async def wrong_meditation_time(message: Message, state: FSMContext) -> None:
    
    await message.answer(
        text="Wrong",
    )
