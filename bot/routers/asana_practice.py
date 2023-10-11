from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import bot.const.phrases as phrases
from bot import markups
from bot.filters import ButtonFilter
from bot.buttons import ChoosePracticeButtons, StepBackButtons


choose_asana_practice_router = Router()

class Asana(StatesGroup):
    count = State()
    asana_time = State()
    relax_time = State()
    shavasana_time = State()


@choose_asana_practice_router.message(ButtonFilter(button=ChoosePracticeButtons.ASANA))
@choose_asana_practice_router.message(ButtonFilter(button=StepBackButtons.ASANACOUNTBACK))
async def asana_practice(message: Message, state:FSMContext) -> None:
    text = phrases.phrase_asana()
    markup = markups.step_back_markup()

    await state.set_state(Asana.count)
    await message.answer(
        text=text,
        reply_markup=markup,    
    )


@choose_asana_practice_router.message(Asana.count, F.text.isdigit())
@choose_asana_practice_router.message(ButtonFilter(button=StepBackButtons.ASANATIMEBACK))
async def enter_asana_count(message: Message, state: FSMContext) -> None:
    count = message.text
    text = phrases.phrase_asana_time()
    markup = markups.step_asana_count_back_markup()
    # await state.clear()
    await state.set_state(Asana.asana_time)
    await message.answer(
        text=text,
        reply_markup=markup,
    )  


@choose_asana_practice_router.message(Asana.count, ~F.text.isdigit()) 
async def wrong_asana_count(message: Message, state: FSMContext) -> None:
    
    await state.set_state(Asana.count)
    await message.answer(
        text="Wrong",
    )


@choose_asana_practice_router.message(Asana.asana_time, F.text.isdigit())
@choose_asana_practice_router.message(ButtonFilter(button=StepBackButtons.ASANARELAXBACK))
async def enter_asana_time(message: Message, state: FSMContext) -> None:
    text = phrases.phrase_asana_relax_time()
    markup = markups.step_asana_time_back_markup()
    asana_time = message.text
    await state.set_state(Asana.relax_time)
    await message.answer(
        text=text,
        reply_markup=markup,
    )


@choose_asana_practice_router.message(Asana.asana_time, ~F.text.isdigit())
async def wrong_asana_time(message: Message, state: FSMContext) -> None:
    await state.set_state(Asana.asana_time)
    await message.answer(
        text="Wrong"
    )


@choose_asana_practice_router.message(Asana.relax_time, F.text.isdigit())
@choose_asana_practice_router.message(ButtonFilter(button=StepBackButtons.SHAVASANABACK))
async def enter_relax_time(message: Message, state: FSMContext) -> None:
    text = phrases.phrase_shavasana_time()
    markup = markups.step_asana_relax_back_markup()
    relax_time = message.text
    await state.set_state(Asana.shavasana_time)
    await message.answer(
        text=text,
        reply_markup=markup,
    )


@choose_asana_practice_router.message(Asana.relax_time, ~F.text.isdigit())
async def wrong_relax_time(message: Message, state: FSMContext) -> None:
    await state.set_state(Asana.relax_time)
    await message.answer(
        text="Wrong"
    )

@choose_asana_practice_router.message(Asana.shavasana_time, F.text.isdigit())
async def enter_shavasana_time(message: Message, state: FSMContext) -> None:
    text = "All RIGTH! Lets start Timer!"
    markup = markups.step_shavasana_back_markup()
    shavasana_time = message.text
    await state.clear()
    await message.answer(
        text=text,
        reply_markup=markup,
    )


@choose_asana_practice_router.message(Asana.shavasana_time, ~F.text.isdigit())
async def wrong_shavasana_time(message: Message, state: FSMContext) -> None:
    await state.set_state(Asana.relax_time)
    await message.answer(
        text="Wrong"
    )


def asana_timer(count, asana_time, relax_time, shasana_time):
    
    pass
