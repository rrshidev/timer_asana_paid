from aiogram import Router
from aiogram.types import Message

import bot.const.phrases as phrases
from bot import markups


meditation_time_router = Router()


@meditation_time_router.message(Message(text=str))
async def medeitation_time(message: Message) -> None:
    text = phrases.phrase_meditation()
    markup = markups.step_back_markup()

    await message.answer(
        text=text,
        reply_markup=markup,    
    )