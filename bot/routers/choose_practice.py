from aiogram import Router
from aiogram.types import Message
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext


import bot.const.phrases as phrases
from bot import markups
from bot.filters import ButtonFilter
from bot.buttons import MainMenuButtons, StepBackButtons


choose_practice_router = Router()


@choose_practice_router.message(
    or_f(
        ButtonFilter(button=MainMenuButtons.PRACTICE_TYPE),
        ButtonFilter(button=StepBackButtons.FULLBACK),
        ButtonFilter(button=StepBackButtons.STEPBACK)
    )
)
async def choose_practice(message: Message, state: FSMContext) -> None:
    await state.clear()
    text = phrases.phrase_for_choose_practice()
    markup = markups.choose_practice_markup()

    await message.answer(
        text=text,
        reply_markup=markup,    
    )

