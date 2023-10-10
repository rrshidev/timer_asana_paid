import asyncio
from asyncio import exceptions
import logging
import re
from typing import Any, Dict

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from bot import const, markups


form_router = Router()


def timer_message(total: int, rest: int = 0, status: bool = True):
    text = f'Идёт медитация\n\nВыбранное время: {total} минут'
    if rest:
        text += f'\n\nОставшееся время: {rest}'
    text += f'\n\nRunning' if status else f'\n\nPaused'

    return text

async def get_time(self, message, count: int):
        sec_count = 60 * count
        
        while sec_count > 0:
            if const.timer_stopped:
                break

            mins, secs = divmod(sec_count, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)

            if not const.timer_paused:        
                sec_count -= 1
                const.timer_rest = timer
                try:
                    await message.edit_text(
                        text=timer_message(total=count, rest=timer, status=not const.timer_paused),
                        reply_markup=markups.practice_stop_process(),
                    )
                except exceptions.MessageNotModified:
                    pass

            await asyncio.sleep(1)
        
        if const.timer_stopped:
            text = "Таймер остановлен!"
            markup = markups.choose_practice()
        if not const.timer_stopped:    
            text = 'Практика окончена!'
            markup = markups.step_back_markup()
            
        return await message.reply(text=text, reply_markup=markup)
    

# @form_router.message()
async def set_meditation_time(message: Message, state: FSMContext) -> None:
    const.timer_stopped = False
    const.timer_paused = False
    time_pattern = r'[+]?\d+$'
    count = int(message.text)
    const.timer_total = count
    if re.fullmatch(time_pattern, message.text):
        edit_message = await message.answer(
            text=timer_message(total=count),
            reply_markup=markups.practice_stop_process(),
        )
        asyncio.create_task(get_time(message=edit_message, count=count))
        await state.finish()
    

@form_router.message(Command(commands=["run"]))
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.name)
    await message.answer(
        text="Hi there! What's your name?",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Command(commands=["cancel"]))
@form_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        text="Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


# @form_router.message(Form.name)
# async def process_name(message: Message, state: FSMContext) -> None:
#     await state.update_data(name=message.text)
#     await state.set_state(Form.like_bots)
#     await message.answer(
#         text=f"Nice to meet you, {html.quote(message.text)}!\nDid you like to write bots?",
#         reply_markup=ReplyKeyboardMarkup(
#             keyboard=[
#                 [
#                     KeyboardButton(text="Yes"),
#                     KeyboardButton(text="No"),
#                 ]
#             ],
#             resize_keyboard=True,
#         ),
#     )


# @form_router.message(Form.like_bots, F.text.casefold() == "no")
# async def process_dont_like_write_bots(message: Message, state: FSMContext) -> None:
#     data = await state.get_data()
#     await state.clear()
#     await message.answer(
#         text="Not bad not terrible.\nSee you soon.",
#         reply_markup=ReplyKeyboardRemove(),
#     )
#     await show_summary(message=message, data=data, positive=False)


# @form_router.message(Form.like_bots, F.text.casefold() == "yes")
# async def process_like_write_bots(message: Message, state: FSMContext) -> None:
#     await state.set_state(Form.language)

#     await message.reply(
#         text="Cool! I'm too!\nWhat programming language did you use for it?",
#         reply_markup=ReplyKeyboardRemove(),
#     )


# @form_router.message(Form.like_bots)
# async def process_unknown_write_bots(message: Message, state: FSMContext) -> None:
#     await message.reply("I don't understand you :(")


# @form_router.message(Form.language)
# async def process_language(message: Message, state: FSMContext) -> None:
#     data = await state.update_data(language=message.text)
#     await state.clear()
#     text = (
#         "Thank for all! Python is in my hearth!\nSee you soon."
#         if message.text.casefold() == "python"
#         else "Thank for information!\nSee you soon."
#     )
#     await message.answer(text=text)
#     await show_summary(message=message, data=data)


async def show_summary(message: Message, data: Dict[str, Any], positive: bool = True) -> None:
    name = data["name"]
    language = data.get("language", "<something unexpected>")
    text = f"I'll keep in mind that, {html.quote(name)}, "
    text += (
        f"you like to write bots with {html.quote(language)}."
        if positive
        else "you don't like to write bots, so sad..."
    )
    await message.answer(
        text=text,
        reply_markup=ReplyKeyboardRemove()
    )
