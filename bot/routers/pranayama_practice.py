from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.logger import logger
from app.services import RedisStorage
import bot.const.phrases as phrases
from bot import markups
from bot.background_tasks import asanaprana_timer_task
from bot.utils import get_redis_entry, str_to_time, get_time_str
from bot.filters import ButtonFilter
from bot.buttons import ChoosePracticeButtons, StepBackButtons
from bot.callbacks import PracticeTimerCallback
from bot.const import enums


choose_pranayama_practice_router = Router()


class PranaYama(StatesGroup):
    count = State()
    prana_time = State()
    reload_time = State()
    meditation_time = State()
    running = State()


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
   
    await state.set_state(PranaYama.prana_time)
    await message.answer(
        text=text,
        reply_markup=markup
    )  


@choose_pranayama_practice_router.message(PranaYama.count, ~F.text.isdigit()) 
async def wrong_prana_count(message: Message, state: FSMContext) -> None:
    
    await state.set_state(PranaYama.count)
    await message.answer(
        text=phrases.phrase_wrong_prana_asana_count(),
    )


@choose_pranayama_practice_router.message(PranaYama.prana_time, F.text.regexp(r'\d+(:\d+)?$'))
@choose_pranayama_practice_router.message(ButtonFilter(button=StepBackButtons.PRANARELOADBACK))
async def enter_prana_time(message: Message, state: FSMContext) -> None:
   
    text = phrases.phrase_prana_reload()
    markup = markups.step_prana_time_back_markup()
      
    await state.update_data(prana_time=message.text)
    await state.set_state(PranaYama.reload_time)
    await message.answer(
        text=text,
        reply_markup=markup
    )  


@choose_pranayama_practice_router.message(PranaYama.prana_time, ~F.text.regexp(r'\d+(:\d+)?$'))
async def wrong_prana_time(message: Message, state: FSMContext) -> None:
    
    await state.set_state(PranaYama.prana_time)
    await message.answer(
        text=phrases.phrase_wrong_prana_asana_time(),
    )

@choose_pranayama_practice_router.message(PranaYama.reload_time, F.text.regexp(r'\d+(:\d+)?$'))
@choose_pranayama_practice_router.message(ButtonFilter(button=StepBackButtons.PRANAMEDITBACK))
async def enter_reload_time(message: Message, state: FSMContext) -> None:
 
    text = phrases.phrase_prana_meditaion_time()
    markup = markups.step_prana_reload_back_markup()
   
    await state.update_data(reload_time=message.text)
    await state.set_state(PranaYama.meditation_time)
    await message.answer(
        text=text,
        reply_markup=markup
    )  


@choose_pranayama_practice_router.message(PranaYama.reload_time, ~F.text.regexp(r'\d+(:\d+)?$'))
async def wrong_reload_time(message: Message, state: FSMContext) -> None:

    await state.set_state(PranaYama.reload_time)
    await message.answer(
        text=phrases.phrase_wrong_prana_asana_time()
    )


@choose_pranayama_practice_router.message(PranaYama.meditation_time, F.text.regexp(r'\d+(:\d+)?$'))
async def enter_meditation_time(message: Message, state: FSMContext) -> None:
   
    gif = FSInputFile("static/pranayama.mp4")
    text = 'Хорошей практики! Начинай дышать... Ом... 🙏'
    markup = markups.step_prana_medit_back_markup()
   
    await state.update_data(meditation_time=message.text)
    await message.answer_animation(gif)
   

    data = await state.get_data()
    
    count = int(data['count'])
    prana_time = int(data['prana_time'])
    reload_time = int(data['reload_time'])
    meditation_time = int(data['meditation_time'])
    
    prana_time_str = str_to_time(input=prana_time)
    reload_time_str = str_to_time(input=reload_time)
    meditation_time_str = str_to_time(input==meditation_time)

    
   
    await state.clear()
    await message.answer(
        text=text,
        reply_markup=markup
        )  


@choose_pranayama_practice_router.message(PranaYama.meditation_time, ~F.text.isdigit()) 
@choose_pranayama_practice_router.message(PranaYama.meditation_time, ~F.text.regexp(r'^[0-5]\d:[0-5]\d$'))
async def wrong_meditation_time(message: Message, state: FSMContext) -> None:
    await state.set_state(PranaYama.meditation_time)
    await message.answer(
        text=phrases.phrase_wrong_meditation(),
    )


async def practice_time(message, data):
   
    count = int(data['count'])
    prana_time = int(data['prana_time'])
    reload_time = int(data['reload_time'])
    meditation_time = int(data['meditation_time'])
    cnt = 0
    count_while = count + 1
    
    while count_while > 0:
        
        if cnt != count:
            
            pt = prana_time
            edit_message = await message.answer(text=f'Идёт практика пранаямы: упражнение №{cnt + 1}')
                
            while pt > -1:
                
                if const.timer_stoped:
                   
                    text = "Таймер остановлен!"
                    markup = markups.choose_practice_markup()
                    break
               
                mins, secs = divmod(pt, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs)
                
                if not const.timer_paused:
                    
                    try:
                        await edit_message.edit_text(text=f'Идёт практика пранаямы: упражнение №{cnt + 1}\n\nОставшееся время: {timer}', reply_markup=markups.practice_stop_process_markup())
                    except:
                        pass
                    pt -= 1
               
                if const.timer_paused:
                   
                    try:
                        await edit_message.edit_text(text=f'Идёт практика пранаямы: упражнение №{cnt + 1}\n\nОставшееся время: {timer}', reply_markup=markups.practice_continue_process_markup())
                    except:
                        pass
                
                time_to_wait = 1 - time.time() % 1
                time.sleep(time_to_wait)

        if cnt != count:
            
            edit_message = await message.answer(text=f'Отдохни! Переведи дух!')
            rt = reload_time
           
            while rt > -1:
                
                if const.timer_stoped:
                    
                    text = "Таймер остановлен!"
                    markup = markups.choose_practice_markup()
                    break
                
                mins, secs = divmod(rt, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs)
               
                if not const.timer_paused:
                    
                    try:
                        await edit_message.edit_text(text=f'Отдохни! Переведи дух!\n\n Сконцентрируйте в одной точке!\n\n\Оставшееся время отдыха: {timer}', reply_markup=markups.practice_stop_process_markup())
                    except:
                        pass
                    rt -= 1
               
                if const.timer_paused:
                    
                    try:
                        await edit_message.edit_text(text=f'Отдохни! Переведи дух!\n\n Сконцентрируйте в одной точке!\n\n\Оставшееся время отдыха: {timer}', reply_markup=markups.practice_continue_process_markup())
                    except:
                        pass
              
                time_to_wait = 1 - time.time() % 1
                time.sleep(time_to_wait)

        if cnt == count:
           
            edit_message = await message.answer(text=f'Медитация...')
            mt = meditation_time
           
            while mt > -1:
                
                if const.timer_stoped:
                    
                    text = "Таймер остановлен!"
                    markup = markups.choose_practice_markup()
                    break
                
                mins, secs = divmod(mt, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs)
               
                if not const.timer_paused:
                   
                    try:
                        await edit_message.edit_text(text=f'Медитация...\n\n иди на свет..\n\n Ом...\n\n Оставшееся время: {timer}', reply_markup=markups.practice_stop_process_markup())
                    except:
                        pass
                    mt -= 1
                    
                if const.timer_paused:
                  
                    try:
                        await edit_message.edit_text(text=f'Медитация...\n\n иди на свет..\n\n Ом...\n\n Оставшееся время: {timer}', reply_markup=markups.practice_continue_process_markup())
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
@choose_pranayama_practice_router.callback_query(lambda c: c.data == 'meditation_pause')
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
@choose_pranayama_practice_router.callback_query(lambda c: c.data == 'meditation_resume')
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


@choose_pranayama_practice_router.callback_query(lambda c: c.data == 'meditation_stop')
async def callback_stop(callback_query: types.CallbackQuery):
    print('Stop world', const.timer_paused, const.timer_stoped)
    if not const.timer_stoped:
        const.timer_stoped = True