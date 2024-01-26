from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from celery.result import AsyncResult

from app.logger import logger
from app.services import RedisStorage
import bot.const.phrases as phrases
from bot import markups
from bot.background_tasks import asana_timer_task
from bot.utils import get_redis_entry, str_to_time, get_time_str
from bot.filters import ButtonFilter
from bot.buttons import ChoosePracticeButtons, StepBackButtons
from bot.callbacks import PracticeTimerCallback
from bot.const import enums


choose_asana_practice_router = Router()


class Asana(StatesGroup):
    count = State()
    practice_time = State()
    reload_time = State()
    meditation_time = State()
    running = State()


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
  
    await state.set_state(Asana.practice_time)
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


@choose_asana_practice_router.message(Asana.practice_time, F.text.regexp(r'\d+(:\d+)?$'))
@choose_asana_practice_router.message(ButtonFilter(button=StepBackButtons.ASANARELAXBACK))
async def enter_asana_time(message: Message, state: FSMContext) -> None:
          
    text = phrases.phrase_asana_relax_time()
    markup = markups.step_asana_time_back_markup()
   
    await state.update_data(practice_time=message.text)
    await state.set_state(Asana.reload_time)
    await message.answer(
        text=text,
        reply_markup=markup,
    )


@choose_asana_practice_router.message(Asana.practice_time, ~F.text.regexp(r'\d+(:\d+)?$'))
async def wrong_asana_time(message: Message, state: FSMContext) -> None:
    
    await state.set_state(Asana.practice_time)
    await message.answer(
        text=phrases.phrase_wrong_prana_asana_time(),
    )

@choose_asana_practice_router.message(Asana.reload_time, F.text.regexp(r'\d+(:\d+)?$'))
@choose_asana_practice_router.message(ButtonFilter(button=StepBackButtons.SHAVASANABACK))
async def enter_relax_time(message: Message, state: FSMContext) -> None:
    
    text = phrases.phrase_shavasana_time()
    markup = markups.step_asana_relax_back_markup()
    
    await state.update_data(reload_time=message.text)
    await state.set_state(Asana.meditation_time)
    await message.answer(
        text=text,
        reply_markup=markup,
    )


@choose_asana_practice_router.message(Asana.reload_time, ~F.text.regexp(r'\d+(:\d+)?$'))
async def wrong_relax_time(message: Message, state: FSMContext) -> None:
   
    await state.set_state(Asana.reload_time)
    await message.answer(
        text=phrases.phrase_wrong_prana_asana_time()
    )

@choose_asana_practice_router.message(Asana.meditation_time, F.text.regexp(r'\d+(:\d+)?$'))
async def enter_shavasana_time(message: Message, state: FSMContext) -> None:
    
    gif = FSInputFile("static/asana.mp4")
    text = "Хорошей практики асан 🙏🏿"
    markup = markups.step_shavasana_back_markup()
        
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
    flag = 'asana_go'
    print('Flag in asana_practice:',flag, 'count:', count)
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
        practice=enums.Practices.ASANA.value,
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

    task: AsyncResult = asana_timer_task.apply_async(
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

    await state.set_state(Asana.running)


@choose_asana_practice_router.message(Asana.meditation_time, ~F.text.regexp(r'\d+(:\d+)?$'))
async def wrong_shavasana_time(message: Message, state: FSMContext) -> None:
    await state.set_state(Asana.meditation_time)
    await message.answer(
        text=phrases.phrase_wrong_meditation(),
    )


#Get callback Pause from markup
@choose_asana_practice_router.callback_query(
        Asana.running, PracticeTimerCallback.filter(F.action == 'pause')
)
async def pause_asana(
    query: CallbackQuery,
    callback_data: PracticeTimerCallback,
    state: FSMContext,
    bot: Bot,
) -> None:
    
    user_entry = get_redis_entry(
        user_id=query.from_user.id,
        practice=enums.Practices.ASANA.value,
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


@choose_asana_practice_router.callback_query(
    Asana.running,
    PracticeTimerCallback.filter(F.action == "stop")
)
async def stop_asana(
    query: CallbackQuery,
    callback_data: PracticeTimerCallback,
    state: FSMContext,
    bot: Bot,
) -> None:
    
    user_entry = get_redis_entry(
        user_id=query.from_user.id,
        practice=enums.Practices.ASANA.value,
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


@choose_asana_practice_router.callback_query(
    Asana.running,
    PracticeTimerCallback.filter(F.action == 'resume')
)
async def resume_asana(
    query: CallbackQuery,
    callback_data: PracticeTimerCallback,
    state: FSMContext,
    bot: Bot,
) -> None:

    user_entry = get_redis_entry(
        user_id=query.from_user.id,
        practice=enums.Practices.ASANA.value,
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

    task: AsyncResult = asana_timer_task.apply_async(
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
