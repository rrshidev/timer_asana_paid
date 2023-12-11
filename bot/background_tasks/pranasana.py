import asyncio
from time import perf_counter

from app.celery_config import celery_app
from app.services import RedisStorage
from app.logger import logger
from bot import markups
from bot.utils import get_redis_entry, get_time_str
from bot.const import phrases, enums

print('check_1')
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
    prana_time: int = int(user_timer_data.get('prana_time'))
    reload_time: int = int(user_timer_data.get('reload_time'))
    meditation_time: int = int(user_timer_data.get('meditation_time'))
    message_id: int = int(user_timer_data.get("message_id"))
    
    base_prana_time = prana_time
    base_reload_time = reload_time

    
    cnt_1 = 0
    count_while = count

    while True:
        start_time = perf_counter()
        if count_while > 0:
                
            rest_pt = base_prana_time
            rest_rt = base_reload_time
            rest_mt = meditation_time
            cnt_1 += 1
            
            print('check_1--->', cnt_1, type(cnt_1))
            
            while True:
                start_time = perf_counter()
                
                if rest_pt > 0:
                    rest_pt -= 1
                
                await bot_instance.edit_message_text(
                    chat_id=user_id,
                    message_id=message_id,
                    text=phrases.phrase_for_pranayama_timer_message(
                        count=count,
                        cnt=cnt_1,
                        prana_time=get_time_str(seconds=rest_pt),
                        reload_time=get_time_str(seconds=rest_rt),
                        meditation_time=get_time_str(seconds=rest_mt),
                        status=enums.TimerStatus.RUNNING, 
                    ),
                    reply_markup=markups.practice_stop_process_markup(),
                )

                RedisStorage.hset(
                    database=3,
                    name=user_entry,
                    mapping=dict(
                        cnt=cnt_1,
                        prana_time=rest_pt,
                    ),
                )

                if rest_pt == 0:
                    await bot_instance.send_message(
                        chat_id=user_id,
                        text="Переведи дух!",
                    )
                    break

                end_time = perf_counter()
                await asyncio.sleep(max(1 - (end_time - start_time), 0))

            while True:
                start_time = perf_counter()
                
                
                if rest_rt > 0:
                    rest_rt -= 1        
                
                await bot_instance.edit_message_text(
                    chat_id=user_id,
                    message_id=message_id,
                    text=phrases.phrase_for_pranayama_timer_message(
                        count=count,
                        cnt=cnt_1,
                        prana_time=get_time_str(seconds=rest_pt),
                        reload_time=get_time_str(seconds=rest_rt),
                        meditation_time=get_time_str(seconds=rest_mt),
                        status=enums.TimerStatus.RUNNING, 
                    ),
                    reply_markup=markups.practice_stop_process_markup(),
                )

                RedisStorage.hset(
                    database=3,
                    name=user_entry,
                    mapping=dict(
                        reload_time=rest_rt,
                    ),
                )
                
                if rest_rt == 0:
                    await bot_instance.send_message(
                        chat_id=user_id,
                        text="Работаем дальше!",
                    )
                    break
                
            
                end_time = perf_counter()
                await asyncio.sleep(max(1 - (end_time - start_time), 0))
            count_while -= 1


        if count_while == 0:
            while True:
                start_time = perf_counter()
                
                if rest_mt > 0:
                    rest_mt -= 1
                
                await bot_instance.edit_message_text(
                    chat_id=user_id,
                    message_id=message_id,
                    text=phrases.phrase_for_pranayama_timer_message(
                        count=count,
                        cnt=cnt_1,
                        prana_time=get_time_str(seconds=rest_pt),
                        reload_time=get_time_str(seconds=rest_rt),
                        meditation_time=get_time_str(seconds=rest_mt),
                        status=enums.TimerStatus.RUNNING, 
                    ),
                    reply_markup=markups.practice_stop_process_markup(),
                )

                RedisStorage.hset(
                    database=3,
                    name=user_entry,
                    mapping=dict(
                        meditation_time=rest_mt,
                    ),
                )

                if rest_mt == 0:
                    break

                end_time = perf_counter()
                await asyncio.sleep(max(1 - (end_time - start_time), 0))
                



        if count_while == 0 and rest_mt == 0: 
            
            await bot_instance.send_message(
                chat_id=user_id,
                text="Практика окончена!",
                reply_markup=markups.choose_practice_markup(),
            )
            break

        end_time = perf_counter()
        await asyncio.sleep(max(1 - (end_time - start_time), 0))

@celery_app.task()
def timer(user_id: int) -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tick(user_id=user_id))
