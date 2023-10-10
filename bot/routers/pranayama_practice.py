from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import bot.const.phrases as phrases
from bot import markups
from bot.filters import ButtonFilter
from bot.buttons import ChoosePracticeButtons


choose_pranayama_practice_router = Router()

class PranaYama(StatesGroup):
    count = State()
    prana_time = State()
    reload = State()
    meditation_time = State()


@choose_pranayama_practice_router.message(ButtonFilter(button=ChoosePracticeButtons.PRANAYAMA))
async def pranayama_practice(message: Message) -> None:
    text = phrases.phrase_pranayama()
    markup = markups.step_back_markup()

    await state.set_state(PranaYama.count)
    await message.answer(
        text=text,
        reply_markup=markup,    
    )

@choose_pranayama_practice_router.message(PranaYama.count, F.text.isdigit())
async def enter_prana_count(message: Message, state: FSMContext) -> None:
    count = message.text
    # await state.clear()
    await state.set_state(PranaYama.prana_time)
    await message.answer(
        text="Right",
    )  


@choose_pranayama_practice_router.message(PranaYama.count, ~F.text.isdigit()) 
async def wrong_prana_count(message: Message, state: FSMContext) -> None:
    
    await state.set_state(PranaYama.count)
    await message.answer(
        text="Wrong",
    )


@choose_pranayama_practice_router.message(PranaYama.prana_time, F.text.isdigit())
async def enter_prana_time(message: Message, state: FSMContext) -> None:
    prana_time = message.text
    # await state.clear()
    await state.set_state(PranaYama.reload)
    await message.answer(
        text="Right",
    )  


@choose_pranayama_practice_router.message(PranaYama.prana_time, ~F.text.isdigit()) 
async def wrong_prana_time(message: Message, state: FSMContext) -> None:
    
    await state.set_state(PranaYama.prana_time)
    await message.answer(
        text="Wrong",
    )

@choose_pranayama_practice_router.message(PranaYama.reload, F.text.isdigit())
async def enter_reload_time(message: Message, state: FSMContext) -> None:
    reload_time = message.text
    # await state.clear()
    await state.set_state(PranaYama.meditation_time)
    await message.answer(
        text="Right",
    )  


@choose_pranayama_practice_router.message(PranaYama.reload, ~F.text.isdigit()) 
async def wrong_reload_time(message: Message, state: FSMContext) -> None:
    
    await state.set_state(PranaYama.reload)
    await message.answer(
        text="Wrong",
    )


@choose_pranayama_practice_router.message(PranaYama.meditation_time, F.text.isdigit())
async def enter_meditation_time(message: Message, state: FSMContext) -> None:
    metation_time = message.text
    # await state.clear()
    await state.finish()
    await message.answer(
        text="Right",
    )  


@choose_pranayama_practice_router.message(PranaYama.reload, ~F.text.isdigit()) 
async def wrong_meditation_time(message: Message, state: FSMContext) -> None:
    
    await state.set_state(PranaYama.reload)
    await message.answer(
        text="Wrong",
    )