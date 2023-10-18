from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import asyncio

import re

import time

import bot.const.phrases as phrases
from bot import markups
from bot.filters import ButtonFilter
from bot.buttons import ChoosePracticeButtons, StepBackButtons
from bot.const import const


choose_pranayama_practice_router = Router()

class PranaYama(StatesGroup):
    count = State()
    prana_time = State()
    reload_time = State()
    meditation_time = State()

def timer_message(total: int, rest: int = 0, status: bool = True):
    text = f'Практика пранаямы!\n\nУпражнение №: {total} мин'
    if rest:
        text += f'\n\nОставшееся время: {rest}'
    text += f'\n\nRunning' if status else f'\n\nPaused'

    return text


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
    await state.update_data(count=message.text)
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
    await state.update_data(prana_time=message.text)
    text = phrases.phrase_prana_reload()
    markup = markups.step_prana_time_back_markup()
    prana_time = message.text
    # await state.clear()
    await state.set_state(PranaYama.reload_time)
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

@choose_pranayama_practice_router.message(PranaYama.reload_time, F.text.isdigit())
@choose_pranayama_practice_router.message(ButtonFilter(button=StepBackButtons.PRANAMEDITBACK))
async def enter_reload_time(message: Message, state: FSMContext) -> None:
    await state.update_data(reload_time=message.text)
    text = phrases.phrase_prana_meditaion_time()
    markup = markups.step_prana_reload_back_markup()
    reload_time = message.text
    # await state.clear()
    await state.set_state(PranaYama.meditation_time)
    await message.answer(
        text=text,
        reply_markup=markup
    )  


@choose_pranayama_practice_router.message(PranaYama.reload_time, ~F.text.isdigit()) 
async def wrong_reload_time(message: Message, state: FSMContext) -> None:
    
    await state.set_state(PranaYama.reload_time)
    await message.answer(
        text="Wrong",
    )


@choose_pranayama_practice_router.message(PranaYama.meditation_time, F.text.isdigit())
async def enter_meditation_time(message: Message, state: FSMContext) -> None:
    await state.update_data(meditation_time=message.text)
    sticker = FSInputFile("static/pranayama.webp")
    gif = FSInputFile("static/breath.mp4")
    text = 'Хорошей практики! Начинай дышать... Ом... 🙏'
    markup = markups.step_prana_medit_back_markup()
    await message.answer_sticker(sticker)
    await message.answer_animation(gif)
    const.timer_stoped = False
    const.timer_paused = False

    data = await state.get_data()

    # edit_message = await message.answer(
    #     text=timer_message(total=total_time),
    #     reply_markup=markups.practice_stop_process_markup(),
    # )
    
    asyncio.create_task(practice_time(message=message, data=data)) #, count=total_time))
    await state.clear()
    await message.answer(
        text=text,
        reply_markup=markup
        )  


@choose_pranayama_practice_router.message(PranaYama.reload_time, ~F.text.isdigit()) 
async def wrong_meditation_time(message: Message, state: FSMContext) -> None:
    await state.set_state(PranaYama.reload_time)
    await message.answer(
        text="Wrong",
    )


async def practice_time(message, data):
    count = int(data['count'])
    prana_time = int(data['prana_time']) * 60
    reload_time = int(data['reload_time'])
    meditation_time = int(data['meditation_time']) * 60  
    cnt = 0
    for i in range(count, 0, -1):
        if const.timer_stoped:
            text = "Таймер остановлен!"
            markup = markups.choose_practice_markup()
            break
        if not const.timer_paused:
            print('Prana #: ', i)
            cnt += 1
            count -= 1
            edit_message = await message.answer(text=f'Идёт практика прнаямы: упражнение №{cnt}')
            while prana_time > 0:
                mins, secs = divmod(prana_time, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs)
                try:
                    await edit_message.edit_text(text=f'Идёт практика прнаямы: упражнение №{cnt}\n\nОставшееся время: {timer}',
                                                 reply_markup=markups.practice_stop_process_markup())
                except:
                    pass
                prana_time -= 1
                time_to_wait = 1 - time.time() % 1
                time.sleep(time_to_wait)
            if cnt != count:
                for countdown in range(reload_time, 0, -1):
                    mins, secs = divmod(countdown, 60)
                    timer = '{:02d}:{:02d}'.format(mins, secs)
                    await edit_message.edit_text(text=f'Отдохни! Переведи дух! Сконцентрируйте в одной точке!\
                                                Оставшееся время отдыха: {timer}',
                                                reply_markup=markups.practice_stop_process_markup())
                    time_to_wait = 1 - time.time() % 1
                    time.sleep(time_to_wait)
            else:
                for countdown in range(meditation_time, 0, -1):
                    mins, secs = divmod(countdown, 60)
                    timer = '{:02d}:{:02d}'.format(mins, secs)
                    await edit_message.edit_text(text=f'Медитация... иди на свет... Ом... \
                                                Оставшееся время Шавасаны: {timer}',
                                                reply_markup=markups.practice_stop_process_markup())
                    time_to_wait = 1 - time.time() % 1
                    time.sleep(time_to_wait)
        else:


    text = 'Практика окончена!'
    markup = markups.choose_practice_markup()
    
    return await message.answer(text=text, reply_markup=markup)
