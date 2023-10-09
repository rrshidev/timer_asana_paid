from aiogram import Router
from aiogram.types import Message

import bot.const.phrases as phrases
from bot import markups
from bot.filters import ButtonFilter
from bot.buttons import MainMenuButtons


choose_practice_router = Router()


@choose_practice_router.message(ButtonFilter(button=MainMenuButtons.PRACTICE_TYPE))
async def choose_practice(message: Message) -> None:
    text = phrases.phrase_for_choose_practice()
    markup = markups.choose_practice_markup()

    await message.answer(
        text=text,
        reply_markup=markup,    
    )
