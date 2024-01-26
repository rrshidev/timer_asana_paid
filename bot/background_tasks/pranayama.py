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
    
    user_timer_data = RedisStorage.hgetall(
            database=3,
            name=user_entry,
        )

    count: int = int(user_timer_data.get('count'))
    cnt: int = int(user_timer_data.get('cnt'))
    practice_time: int = int(user_timer_data.get('practice_time'))
    reload_time: int = int(user_timer_data.get('reload_time'))
    meditation_time: int = int(user_timer_data.get('meditation_time'))
    flag: str = str(user_timer_data.get('flag'))
    message_id: int = int(user_timer_data.get('message_id'))
    print('FLAG-->', '111222333',flag)
    base_practice_time = practice_time
    base_reload_time = reload_time
    cnt_1 = cnt
    count_while = count
    print('count_while:', count_while)

    while True:
    
        if count_while > 0:

            count_while -= 1 
            rest_pt = base_practice_time
            rest_rt = base_reload_time
            
            cnt_1 += 1
                        
            while rest_pt > -1:
                
                start_time = perf_counter()
                flag = 'go'
                
                await bot_instance.edit_message_text(
                    chat_id=user_id,
                    message_id=message_id,
                    text=phrases.phrase_for_pranasana_timer_message(
                        count=count,
                        cnt=cnt_1,
                        practice_time=get_time_str(seconds=rest_pt),
                        reload_time=get_time_str(seconds=rest_rt),
                        meditation_time=get_time_str(seconds=meditation_time),
                        flag = flag,
                        status=enums.TimerStatus.RUNNING, 
                    ),
                    reply_markup=markups.practice_stop_process_markup(),
                )
                rest_pt -= 1
                
                RedisStorage.hset(
                    database=3,
                    name=user_entry,
                    mapping=dict(
                        cnt=cnt_1,
                        practice_time=rest_pt,
                        flag = flag,
                    ),
                )
            
                if rest_pt == -1:

                    await bot_instance.send_message(
                        chat_id=user_id,
                        text="Переведи дух!",
                    )
            
                end_time = perf_counter()
                await asyncio.sleep(max(1 - (end_time - start_time), 0))

            while rest_rt > -1:
                
                start_time = perf_counter()
                flag = 'relax'
                
                await bot_instance.edit_message_text(
                    chat_id=user_id,
                    message_id=message_id,
                    text=phrases.phrase_for_pranasana_timer_message(
                        count=count,
                        cnt=cnt_1,
                        practice_time=get_time_str(seconds=rest_pt),
                        reload_time=get_time_str(seconds=rest_rt),
                        meditation_time=get_time_str(seconds=meditation_time),
                        flag = flag,
                        status=enums.TimerStatus.RUNNING,                    
                    ),
                    reply_markup=markups.practice_stop_process_markup(),
                )
                rest_rt -= 1
                
                RedisStorage.hset(
                    database=3,
                    name=user_entry,
                    mapping=dict(
                        reload_time=rest_rt,
                        flag=flag,
                    ),
                )
                
                if rest_rt == -1:

                    await bot_instance.send_message(
                        chat_id=user_id,
                        text="Работаем дальше!",
                    )
            
                end_time = perf_counter()
                await asyncio.sleep(max(1 - (end_time - start_time), 0))
        print(count_while)
        if count_while == 0:

            await bot_instance.send_message(
                chat_id=user_id,
                text="Медитация!",
            )
            
            while meditation_time > -1:
                
                start_time = perf_counter()
                flag = 'meditation'
                
                await bot_instance.edit_message_text(
                    chat_id=user_id,
                    message_id=message_id,
                    text=phrases.phrase_for_pranasana_timer_message(
                        count=count,
                        cnt=cnt_1,
                        practice_time=get_time_str(seconds=practice_time),
                        reload_time=get_time_str(seconds=reload_time),
                        meditation_time=get_time_str(seconds=meditation_time),
                        flag=flag,
                        status=enums.TimerStatus.RUNNING, 
                    ),
                    reply_markup=markups.practice_stop_process_markup(),
                )
                
                meditation_time -= 1
                
                RedisStorage.hset(
                    database=3,
                    name=user_entry,
                    mapping=dict(
                        meditation_time=meditation_time,
                        flag=flag,
                    ),
                )         
                
                end_time = perf_counter()
                await asyncio.sleep(max(1 - (end_time - start_time), 0))       
        
            await bot_instance.send_message(
                chat_id=user_id,
                text="Практика окончена!",
                reply_markup=markups.choose_practice_markup(),
            )
            break


@celery_app.task()
def timer(user_id: int) -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tick(user_id=user_id))
