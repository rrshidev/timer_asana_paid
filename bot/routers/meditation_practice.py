import re

from aiogram import Router, F, types
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import asyncio

import time

import bot.const.phrases as phrases
from bot import markups
from bot.filters import ButtonFilter
from bot.buttons import ChoosePracticeButtons
from bot.const import const


choose_meditation_practice_router = Router()


class Meditation(StatesGroup):
    time = State()


def timer_message(total, rest: int = 0, status: bool = True):
    text = f'Идёт медитация\n\nВыбранное время: {total}'
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
@choose_meditation_practice_router.message(Meditation.time, F.text.regexp(r'^[0-5]\d:[0-5]\d$'))
async def enter_meditation_time(message: Message, state: FSMContext) -> None:
       
    const.timer_stoped = False
    const.timer_paused = False

    time_pattern = r'^\d{2}:\d{2}$'
    
    if re.match(time_pattern, message.text):

        mins, secs = (message.text.split(':'))
        total_time = int(mins)*60 + int(secs)
    
    else:

        total_time = int(message.text) * 60

    gif = FSInputFile("static/meditation.mp4")
    await message.answer_animation(gif)

    edit_message = await message.answer(
        text=timer_message(total=total_time),
        reply_markup=markups.practice_stop_process_markup(),
    )
    asyncio.create_task(get_time(message=edit_message, count=total_time))
    await state.clear()


async def get_time(message, count):
        
        sec_count = count
        seconds = count
        minutes = seconds // 60
        seconds %= 60
        timer_total = '{:02d} мин. {:02d} сек.'.format(minutes, seconds)
        
        while sec_count > 0:

            if const.timer_stoped:
                break

            mins, secs = divmod(sec_count, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)

            if not const.timer_paused:        
                sec_count -= 1
                const.timer_rest = timer
                try:
                    await message.edit_text(
                        text=timer_message(total=timer_total, rest=timer, status=not const.timer_paused),
                        reply_markup=markups.practice_stop_process_markup(),
                    )
                except:
                    pass

            if const.timer_paused:        
                const.timer_rest = timer
                try:
                    await message.edit_text(
                        text=timer_message(total=timer_total, rest=timer, status=not const.timer_paused),
                        reply_markup=markups.practice_continue_process_markup(),
                    )
                except:
                    pass

            time_to_wait = 1 - time.time() % 1
            time.sleep(time_to_wait)

        
        if const.timer_stoped:
            text = "Таймер остановлен!"
            markup = markups.choose_practice_markup()
        if not const.timer_stoped:    
            print('test3', const.timer_paused, const.timer_stoped)
            text = 'Практика окончена!'
            markup = markups.choose_practice_markup()
            
        return await message.reply(text=text, reply_markup=markup)



#Get callback Pause from markup
@choose_meditation_practice_router.callback_query(lambda c: c.data == 'meditation_pause')
async def callback_pause(callback_query: types.CallbackQuery):
    print('Pause world', const.timer_paused, const.timer_stoped)
    if not const.timer_paused:
        const.timer_paused = True
        await callback_query.message.edit_text(
            text=timer_message(
                total=const.timer_total,
                rest=const.timer_rest,
                status=False,
            ),
            reply_markup=markups.practice_continue_process_markup(),
        )


#Get callback Resume markup
@choose_meditation_practice_router.callback_query(lambda c: c.data == 'meditation_resume')
async def callback_resume(callback_query: types.CallbackQuery):
    print('Resume world', const.timer_paused, const.timer_stoped)

    if const.timer_paused:
        const.timer_paused = False
        await callback_query.message.edit_text(
            text=timer_message(
                total=const.timer_total,
                rest=const.timer_rest,
                status=True,
            ),
            reply_markup=markups.practice_stop_process_markup(),
        )


@choose_meditation_practice_router.callback_query(lambda c: c.data == 'meditation_stop')
async def callback_stop(callback_query: types.CallbackQuery):
    print('Stop world', const.timer_paused, const.timer_stoped)
    if not const.timer_stoped:
        const.timer_stoped = True


@choose_meditation_practice_router.message(Meditation.time, ~F.text.isdigit())
@choose_meditation_practice_router.message(Meditation.time, ~F.text.regexp(r'^\d{2}:\d{2}$'))
async def wrong_meditation_time(message: Message, state: FSMContext) -> None:
    
    await state.set_state(Meditation.time)
    await message.answer(
        text=phrases.phrase_wrong_meditation()
    )



