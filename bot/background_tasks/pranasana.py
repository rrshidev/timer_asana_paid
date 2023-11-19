import asyncio
from time import perf_counter

from app.celery_config import celery_app
from app.services import RedisStorage
from app.logger import logger
from bot import markups
from bot.utils import get_redis_entry, get_time_str
from bot.const import phrases, enums


async def tick(user_id: id) -> None:
    from bot import bot_instance

    user_entry = get_redis_entry(
        user_id=user_id,
        practice=enums.Practices.PRANAYAMA.value,
    )

    while True:
        start_time = perf_counter()
        user_timer_data = RedisStorage.hgerall(
            database=3,
            name=user_entry,
        )

        cnt: int = int(user_timer_data.get('cnt'))
        prana_time: int = int(user_timer_data.get('prana_time'))
        reload_time: int = int(user_timer_data.get('reload_time'))
        meditation_time: inr = int(user_timer_data.get('meditation_time'))
        message_id: int = int(user_timer_data.get("messsage_id"))

        

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



@celery_app.task()
def timer(user_id: int) -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tick(user_id=user_id))
