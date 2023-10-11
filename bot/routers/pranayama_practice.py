from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import bot.const.phrases as phrases
from bot import markups
from bot.filters import ButtonFilter
from bot.buttons import ChoosePracticeButtons, StepBackButtons


choose_pranayama_practice_router = Router()

class PranaYama(StatesGroup):
    count = State()
    prana_time = State()
    reload = State()
    meditation_time = State()


@choose_pranayama_practice_router.message(ButtonFilter(button=ChoosePracticeButtons.PRANAYAMA))
@choose_pranayama_practice_router.message(ButtonFilter(button=StepBackButtons.PRANACOUNTBACK))
async def pranayama_practice(message: Message, state: FSMContext) -> None:
    text = phrases.phrase_pranayama()
    markup = markups.step_back_markup()
    await state.set_state(PranaYama.count)
    await message.answer(
        text=text,
        reply_markup=markup,    
    )


@choose_pranayama_practice_router.message(PranaYama.count, F.text.isdigit())
@choose_pranayama_practice_router.message(ButtonFilter(button=StepBackButtons.PRANATIMEBACK))
async def enter_prana_count(message: Message, state: FSMContext) -> None:
    text = phrases.phrase_prana_time()
    markup = markups.step_prana_count_back_markup()
    count = message.text
    await state.set_state(PranaYama.prana_time)
    await message.answer(
        text=text,
        reply_markup=markup
    )  


@choose_pranayama_practice_router.message(PranaYama.count, ~F.text.isdigit()) 
async def wrong_prana_count(message: Message, state: FSMContext) -> None:
    
    await state.set_state(PranaYama.count)
    await message.answer(
        text="Wrong",
    )


@choose_pranayama_practice_router.message(PranaYama.prana_time, F.text.isdigit())
@choose_pranayama_practice_router.message(ButtonFilter(button=StepBackButtons.PRANARELOADBACK))
async def enter_prana_time(message: Message, state: FSMContext) -> None:
    text = phrases.phrase_prana_reload()
    markup = markups.step_prana_time_back_markup()
    prana_time = message.text
    # await state.clear()
    await state.set_state(PranaYama.reload)
    await message.answer(
        text=text,
        reply_markup=markup
    )  


@choose_pranayama_practice_router.message(PranaYama.prana_time, ~F.text.isdigit()) 
async def wrong_prana_time(message: Message, state: FSMContext) -> None:
    
    await state.set_state(PranaYama.prana_time)
    await message.answer(
        text="Wrong",
    )

@choose_pranayama_practice_router.message(PranaYama.reload, F.text.isdigit())
@choose_pranayama_practice_router.message(ButtonFilter(button=StepBackButtons.PRANAMEDITBACK))
async def enter_reload_time(message: Message, state: FSMContext) -> None:
    text = phrases.phrase_prana_meditaion_time()
    markup = markups.step_prana_reload_back_markup()
    reload_time = message.text
    # await state.clear()
    await state.set_state(PranaYama.meditation_time)
    await message.answer(
        text=text,
        reply_markup=markup
    )  


@choose_pranayama_practice_router.message(PranaYama.reload, ~F.text.isdigit()) 
async def wrong_reload_time(message: Message, state: FSMContext) -> None:
    
    await state.set_state(PranaYama.reload)
    await message.answer(
        text="Wrong",
    )


@choose_pranayama_practice_router.message(PranaYama.meditation_time, F.text.isdigit())
async def enter_meditation_time(message: Message, state: FSMContext) -> None:
    text = 'All rigth! GO GO GO Timer!'
    markup = markups.step_prana_medit_back_markup()
    metation_time = message.text
    await state.clear()
    await message.answer(
        text=text,
        reply_markup=markup
        )  


@choose_pranayama_practice_router.message(PranaYama.reload, ~F.text.isdigit()) 
async def wrong_meditation_time(message: Message, state: FSMContext) -> None:
    
    await state.set_state(PranaYama.reload)
    await message.answer(
        text="Wrong",
    )