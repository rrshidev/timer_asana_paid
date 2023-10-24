import re

from aiogram import Router, F, types
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import asyncio

import time

import bot.const.phrases as phrases
from bot import markups
from bot.filters import ButtonFilter
from bot.buttons import ChoosePracticeButtons, StepBackButtons
from bot.const import const


choose_asana_practice_router = Router()

time_pattern = r'^\d{2}:\d{2}$'

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
    await state.update_data(count=message.text)
  
    text = phrases.phrase_asana_time()
    markup = markups.step_asana_count_back_markup()
  
    await state.set_state(Asana.asana_time)
    await message.answer(
        text=text,
        reply_markup=markup,
    )  


@choose_asana_practice_router.message(Asana.count, ~F.text.isdigit()) 
async def wrong_asana_count(message: Message, state: FSMContext) -> None:
    
    await state.set_state(Asana.count)
    await message.answer(
        text=phrases.phrase_wrong_prana_asana_count(),
    )


@choose_asana_practice_router.message(Asana.asana_time, F.text.isdigit())
@choose_asana_practice_router.message(Asana.asana_time, F.text.regexp(r'^[0-5]\d:[0-5]\d$'))
@choose_asana_practice_router.message(ButtonFilter(button=StepBackButtons.ASANARELAXBACK))
async def enter_asana_time(message: Message, state: FSMContext) -> None:

    if re.match(time_pattern, message.text):
        
        mins, secs = (message.text.split(':'))
        total_time = int(mins)*60 + int(secs)
        await state.update_data(asana_time=total_time)
    
    else:
        
        await state.update_data(asana_time=message.text)
        
    text = phrases.phrase_asana_relax_time()
    markup = markups.step_asana_time_back_markup()
   
    await state.set_state(Asana.relax_time)
    await message.answer(
        text=text,
        reply_markup=markup,
    )


@choose_asana_practice_router.message(Asana.asana_time, ~F.text.isdigit())
@choose_asana_practice_router.message(Asana.asana_time, ~F.text.regexp(r'^[0-5]\d:[0-5]\d$'))

async def wrong_asana_time(message: Message, state: FSMContext) -> None:
    await state.set_state(Asana.asana_time)
    await message.answer(
        text=phrases.phrase_wrong_prana_asana_time()
    )


@choose_asana_practice_router.message(Asana.relax_time, F.text.isdigit())
@choose_asana_practice_router.message(Asana.relax_time, F.text.regexp(r'^[0-5]\d:[0-5]\d$'))
@choose_asana_practice_router.message(ButtonFilter(button=StepBackButtons.SHAVASANABACK))
async def enter_relax_time(message: Message, state: FSMContext) -> None:
    
    if re.match(time_pattern, message.text):
        
        mins, secs = (message.text.split(':'))
        total_time = int(mins)*60 + int(secs)
        await state.update_data(relax_time=total_time)
    
    else:
        
        await state.update_data(relax_time=message.text)

    text = phrases.phrase_shavasana_time()
    markup = markups.step_asana_relax_back_markup()
    
    await state.set_state(Asana.shavasana_time)
    await message.answer(
        text=text,
        reply_markup=markup,
    )


@choose_asana_practice_router.message(Asana.relax_time, ~F.text.isdigit())
@choose_asana_practice_router.message(Asana.relax_time, ~F.text.regexp(r'^[0-5]\d:[0-5]\d$'))
async def wrong_relax_time(message: Message, state: FSMContext) -> None:
   
    await state.set_state(Asana.relax_time)
    await message.answer(
        text=phrases.phrase_wrong_prana_asana_time()
    )

@choose_asana_practice_router.message(Asana.shavasana_time, F.text.isdigit())
@choose_asana_practice_router.message(Asana.shavasana_time, F.text.regexp(r'^[0-5]\d:[0-5]\d$'))
async def enter_shavasana_time(message: Message, state: FSMContext) -> None:
    
    if re.match(time_pattern, message.text):
        
        mins, secs = (message.text.split(':'))
        total_time = int(mins)*60 + int(secs)
        await state.update_data(shavasana_time=total_time)
    
    else:
        
        await state.update_data(shavasana_time=message.text)
    
    gif = FSInputFile("static/asana.mp4")
    text = "Хорошей практики асан 🙏🏿"
    markup = markups.step_shavasana_back_markup()

    await message.answer_animation(gif)

    const.timer_stoped = False
    const.timer_paused = False

    data = await state.get_data()

    asyncio.create_task(asana_timer(message=message, data=data))

    await state.clear()
    await message.answer(
        text=text,
        reply_markup=markup,
    )


@choose_asana_practice_router.message(Asana.shavasana_time, ~F.text.isdigit())
@choose_asana_practice_router.message(Asana.shavasana_time, ~F.text.regexp(r'^[0-5]\d:[0-5]\d$'))
async def wrong_shavasana_time(message: Message, state: FSMContext) -> None:
    await state.set_state(Asana.shavasana_time)
    await message.answer(
        text=phrases.phrase_wrong_meditation()
    )


async def asana_timer(message, data):
    
    count = int(data['count'])
    asana_time = int(data['asana_time'])
    relax_time = int(data['relax_time'])
    shavasana_time = int(data['shavasana_time'])
    cnt = 0
    count_while = count + 1

    while count_while > 0:
        
        if cnt != count:
            
            at = asana_time
            edit_message = await message.answer(text=f'Идёт практика асаны: упражнение №{cnt + 1}')
                
            while at > -1:
                
                if const.timer_stoped:
                   
                    text = "Таймер остановлен!"
                    markup = markups.choose_practice_markup()
                    break
               
                mins, secs = divmod(at, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs)
                
                if not const.timer_paused:
                    
                    try:
                        await edit_message.edit_text(text=f'Идёт практика асаны: Асана №{cnt + 1}\n\nОставшееся время: {timer}', reply_markup=markups.practice_stop_process_markup())
                    except:
                        pass
                    at -= 1
               
                if const.timer_paused:
                   
                    try:
                        await edit_message.edit_text(text=f'Идёт практика асаны: Асана №{cnt + 1}\n\nОставшееся время: {timer}', reply_markup=markups.practice_continue_process_markup())
                    except:
                        pass
                
                time_to_wait = 1 - time.time() % 1
                time.sleep(time_to_wait)

        if cnt != count:
            
            edit_message = await message.answer(text=f'Компенсирующая асана или шавасана - на твой выбор!')
            rt = relax_time
           
            while rt > -1:
                
                if const.timer_stoped:
                    
                    text = "Таймер остановлен!"
                    markup = markups.choose_practice_markup()
                    break
                
                mins, secs = divmod(rt, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs)
               
                if not const.timer_paused:
                    
                    try:
                        await edit_message.edit_text(text=f'Компенсирующая асана или шавасана - на твой выбор!\n\n\Оставшееся время отдыха: {timer}', reply_markup=markups.practice_stop_process_markup())
                    except:
                        pass
                    rt -= 1
               
                if const.timer_paused:
                    
                    try:
                        await edit_message.edit_text(text=f'Компенсирующая асана или шавасана - на твой выбор!\n\n\Оставшееся время отдыха: {timer}', reply_markup=markups.practice_continue_process_markup())
                    except:
                        pass
              
                time_to_wait = 1 - time.time() % 1
                time.sleep(time_to_wait)

        if cnt == count:
           
            edit_message = await message.answer(text=f'Шавасана...\n\nВыдыхай, концентрируйся, собирайся в точку')
            st = shavasana_time
           
            while st > -1:
                
                if const.timer_stoped:
                    
                    text = "Таймер остановлен!"
                    markup = markups.choose_practice_markup()
                    break
                
                mins, secs = divmod(st, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs)
               
                if not const.timer_paused:
                   
                    try:
                        await edit_message.edit_text(text=f'Шавасана...\n\nВыдыхай, концентрируйся, собирайся в точку\n\n Оставшееся время: {timer}', reply_markup=markups.practice_stop_process_markup())
                    except:
                        pass
                    st -= 1
                    
                if const.timer_paused:
                  
                    try:
                        await edit_message.edit_text(text=f'Шавасана...\n\nВыдыхай, концентрируйся, собирайся в точку\n\n Оставшееся время: {timer}', reply_markup=markups.practice_continue_process_markup())
                    except:
                        pass
               
                time_to_wait = 1 - time.time() % 1
                time.sleep(time_to_wait)
       
        cnt += 1
        count_while -= 1                

    text = 'Практика окончена!'
    markup = markups.choose_practice_markup()
    
    return await message.answer(text=text, reply_markup=markup)
    

    #Get callback Pause from markup
@choose_asana_practice_router.callback_query(lambda c: c.data == 'meditation_pause')
async def callback_pause(callback_query: types.CallbackQuery):
    print('Pause world', const.timer_paused, const.timer_stoped)
    if not const.timer_paused:
        const.timer_paused = True
        # await callback_query.message.edit_text(
        #     text=timer_message(
        #         total=const.timer_total,
        #         rest=const.timer_rest,
        #         status=False,
        #     ),
        #     reply_markup=markups.practice_continue_process_markup(),
        # )


#Get callback Resume markup
@choose_asana_practice_router.callback_query(lambda c: c.data == 'meditation_resume')
async def callback_resume(callback_query: types.CallbackQuery):
    print('Resume world', const.timer_paused, const.timer_stoped)

    if const.timer_paused:
        const.timer_paused = False
        # await callback_query.message.edit_text(
        #     text=timer_message(
        #         total=const.timer_total,
        #         rest=const.timer_rest,
        #         status=True,
        #     ),
        #     reply_markup=markups.practice_stop_process_markup(),
        # )


@choose_asana_practice_router.callback_query(lambda c: c.data == 'meditation_stop')
async def callback_stop(callback_query: types.CallbackQuery):
    print('Stop world', const.timer_paused, const.timer_stoped)
    if not const.timer_stoped:
        const.timer_stoped = True
