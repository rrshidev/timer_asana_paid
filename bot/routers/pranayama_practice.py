from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from celery.result import AsyncResult

from app.logger import logger
from app.services import RedisStorage
import bot.const.phrases as phrases
from bot import markups
from bot.background_tasks import pranayama_timer_task
from bot.utils import get_redis_entry, str_to_time, get_time_str
from bot.filters import ButtonFilter
from bot.buttons import ChoosePracticeButtons, StepBackButtons
from bot.callbacks import PracticeTimerCallback
from bot.const import enums


choose_pranayama_practice_router = Router()


class PranaYama(StatesGroup):
    count = State()
    practice_time = State()
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
   
    await state.set_state(PranaYama.practice_time)
    await message.answer(
        text=text,
        reply_markup=markup,
    )  


@choose_pranayama_practice_router.message(PranaYama.count, ~F.text.isdigit()) 
async def wrong_prana_count(message: Message, state: FSMContext) -> None:
    
    await state.set_state(PranaYama.count)
    await message.answer(
        text=phrases.phrase_wrong_prana_asana_count(),
    )


@choose_pranayama_practice_router.message(PranaYama.practice_time, F.text.regexp(r'\d+(:\d+)?$'))
@choose_pranayama_practice_router.message(ButtonFilter(button=StepBackButtons.PRANARELOADBACK))
async def enter_prana_time(message: Message, state: FSMContext) -> None:
   
    text = phrases.phrase_prana_reload()
    markup = markups.step_prana_time_back_markup()
      
    await state.update_data(practice_time=message.text)
    await state.set_state(PranaYama.reload_time)
    await message.answer(
        text=text,
        reply_markup=markup
    )  


@choose_pranayama_practice_router.message(PranaYama.practice_time, ~F.text.regexp(r'\d+(:\d+)?$'))
async def wrong_prana_time(message: Message, state: FSMContext) -> None:
    
    await state.set_state(PranaYama.practice_time)
    await message.answer(
        text=phrases.phrase_wrong_prana_asana_time(),
    )

@choose_pranayama_practice_router.message(PranaYama.reload_time, F.text.regexp(r'\d+(:\d+)?$'))
@choose_pranayama_practice_router.message(ButtonFilter(button=StepBackButtons.PRANAMEDITBACK))
async def enter_reload_time(message: Message, state: FSMContext) -> None:
 
    text = phrases.phrase_prana_meditation_time()
    markup = markups.step_prana_reload_back_markup()
   
    await state.update_data(reload_time=message.text)
    await state.set_state(PranaYama.meditation_time)
    await message.answer(
        text=text,
        reply_markup=markup,
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
    practice_time = data['practice_time']
    reload_time = data['reload_time']
    meditation_time = data['meditation_time']
    
    cnt = 0
    
    right_practice_time = str_to_time(practice_time)
    right_reload_time = str_to_time(reload_time)
    right_meditation_time = str_to_time(meditation_time)

    practice_time_str = get_time_str(seconds=right_practice_time.total_seconds())
    reload_time_str = get_time_str(seconds=right_reload_time.total_seconds())
    meditation_time_str = get_time_str(seconds=right_meditation_time.total_seconds())
    flag = 'go'
    edit_message = await message.answer(
        text=phrases.phrase_for_pranasana_timer_message(
            count=count,
            cnt=cnt,
            practice_time=practice_time_str,
            reload_time=reload_time_str,
            meditation_time=meditation_time_str,
            flag=flag,
            status=enums.TimerStatus.RUNNING,
        ),
        reply_markup=markups.practice_stop_process_markup(),
    )

    user_entry = get_redis_entry(
        user_id=message.from_user.id,
        practice=enums.Practices.PRANAYAMA.value,
    )
    
    RedisStorage.hset(
        database=3,
        name=user_entry,
        mapping=dict(
            count=count,
            cnt=cnt,
            practice_time=int(right_practice_time.total_seconds()),
            reload_time=int(right_reload_time.total_seconds()),
            meditation_time=int(right_meditation_time.total_seconds()),
            flag=flag,
            message_id=edit_message.message_id,
        )
    )

    task: AsyncResult = pranayama_timer_task.apply_async(
        args=[message.from_user.id],
        countdown=0,
    )

    RedisStorage.hset(
        database=3,
        name=user_entry,
        mapping=dict(
            task_id=task.id,
        ),
    )

    await state.set_state(PranaYama.running)      


@choose_pranayama_practice_router.message(PranaYama.meditation_time, ~F.text.regexp(r'\d+(:\d+)?$'))
async def wrong_meditation_time(message: Message, state: FSMContext) -> None:
    await state.set_state(PranaYama.meditation_time)
    await message.answer(
        text=phrases.phrase_wrong_meditation(),
    )


#Get callback Pause from markup
@choose_pranayama_practice_router.callback_query(
        PranaYama.running, PracticeTimerCallback.filter(F.action == "pause")
)
async def pause_pranayama(
    query: CallbackQuery,
    callback_data: PracticeTimerCallback,
    state: FSMContext,
    bot: Bot,
) -> None:
    
    user_entry = get_redis_entry(
        user_id=query.from_user.id,
        practice=enums.Practices.PRANAYAMA.value,
    )
    user_timer_data = RedisStorage.hgetall(
        database=3,
        name=user_entry,
    )

    AsyncResult(user_timer_data.get("task_id")).revoke(terminate=True)
    message_id: int = user_timer_data.get("message_id")
    count = int(user_timer_data.get('count'))
    cnt = int(user_timer_data.get('cnt'))
    practice_time_str = get_time_str(seconds=int(user_timer_data.get('practice_time')))
    reload_time_str = get_time_str(seconds=int(user_timer_data.get('reload_time')))
    meditation_time_str = get_time_str(seconds=int(user_timer_data.get('meditation_time')))
    flag = str(user_timer_data.get('flag'))

    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=message_id,
        text=phrases.phrase_for_pranasana_timer_message(
            count=count,
            cnt=cnt,
            practice_time=practice_time_str,
            reload_time=reload_time_str,
            meditation_time=meditation_time_str,
            status=enums.TimerStatus.PAUSED,
            flag = flag,
        ),
        reply_markup=markups.practice_continue_process_markup(),
    )

    await query.answer()


@choose_pranayama_practice_router.callback_query(
    PranaYama.running, 
    PracticeTimerCallback.filter(F.action == "stop")
)
async def stop_pranayama(
    query: CallbackQuery,
    callback_data: PracticeTimerCallback,
    state: FSMContext,
    bot: Bot,
) -> None:
    
    user_entry = get_redis_entry(
        user_id=query.from_user.id,
        practice=enums.Practices.PRANAYAMA.value,
    )
    user_timer_data = RedisStorage.hgetall(
        database=3,
        name=user_entry,
    )

    AsyncResult(user_timer_data.get("task_id")).revoke(terminate=True)
    message_id: int = user_timer_data.get("message_id")
    count = int(user_timer_data.get('count'))
    cnt = int(user_timer_data.get('cnt'))
    practice_time_str = get_time_str(seconds=int(user_timer_data.get('practice_time')))
    reload_time_str = get_time_str(seconds=int(user_timer_data.get('reload_time')))
    meditation_time_str = get_time_str(seconds=int(user_timer_data.get('meditation_time')))
    flag = str(user_timer_data.get('flag'))

    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=message_id,
        text=phrases.phrase_for_pranasana_timer_message(
            count=count,
            cnt=cnt,
            practice_time=practice_time_str,
            reload_time=reload_time_str,
            meditation_time=meditation_time_str,
            status=enums.TimerStatus.STOPPED,
            flag = flag,
        ),
        reply_markup=None,
    )
    await bot.send_message(
        chat_id=query.from_user.id,
        text="Практика окончена!",
        reply_markup=markups.choose_practice_markup(),
    )

    RedisStorage.hset(
        database=3,
        name=user_entry,
        mapping=dict(
            count=0,
            cnt=0,
            practice_time=0,
            reload_time=0,
            meditation_time=0,
        ), 
    )

    await query.answer()

#Get callback Resume markup
@choose_pranayama_practice_router.callback_query(
        PranaYama.running,
        PracticeTimerCallback.filter(F.action == "resume")
)
async def resume_pranayama(
    query: CallbackQuery,
    callback_data: PracticeTimerCallback,
    state: FSMContext,
    bot: Bot,
) -> None:
    
    user_entry = get_redis_entry(
        user_id=query.from_user.id,
        practice=enums.Practices.PRANAYAMA.value,
    )
    user_timer_data = RedisStorage.hgetall(
        database=3,
        name=user_entry,
    )

    message_id: int = user_timer_data.get("message_id")
    count = int(user_timer_data.get('count'))
    cnt = int(user_timer_data.get('cnt'))
    practice_time_str = get_time_str(seconds=int(user_timer_data.get('practice_time')))
    reload_time_str = get_time_str(seconds=int(user_timer_data.get('reload_time')))
    meditation_time_str = get_time_str(seconds=int(user_timer_data.get('meditation_time')))
    flag = str(user_timer_data.get('flag'))

    await bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=message_id,
        text=phrases.phrase_for_pranasana_timer_message(
            count=count,
            cnt=cnt,
            practice_time=practice_time_str,
            reload_time=reload_time_str,
            meditation_time=meditation_time_str,
            status=enums.TimerStatus.RUNNING,
            flag=flag,
        ),
        reply_markup=markups.practice_stop_process_markup(),
    )

    task: AsyncResult = pranayama_timer_task.apply_async(
        args=[query.from_user.id],
        countdown=0,
    )

    RedisStorage.hset(
        database=3,
        name=user_entry,
        mapping=dict(
            task_id=task.id,
        ),
    )

    await query.answer()


