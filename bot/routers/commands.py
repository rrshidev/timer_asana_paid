from aiogram import Router, Bot
from aiogram.types import Message, FSInputFile, MenuButtonWebApp, WebAppInfo
from aiogram.filters import Command, ExceptionMessageFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from app.database.orm import UserModel
import bot.const.phrases as phrases
from bot import markups
from bot.filters import ButtonFilter
from bot.buttons import ChoosePracticeButtons


commands_router = Router()

@commands_router.message(Command(commands=["start"]))
@commands_router.message(ButtonFilter(button=ChoosePracticeButtons.BACK))
async def start(message: Message, bot: Bot, session: AsyncSession) -> None:
    first_name = message.from_user.first_name
    markup = markups.user_main_markup()
    text = phrases.phrase_for_start_first_greeting(data=dict(name=first_name))

    # check if user exists
    user = (
        await session.execute(
            select(UserModel).where(UserModel.tg_id.__eq__(message.from_user.id))
        )
    ).scalar()

    # if not => create
    if not user:
        await session.execute(
            insert(UserModel)
            .values(
                {
                    UserModel.first_name: first_name,
                    UserModel.tg_id: message.from_user.id,
                    UserModel.tg_username: message.from_user.username,
                    UserModel.is_admin: False,
                    UserModel.timer_stoped: False,
                    UserModel.timer_paused: False,
                }
            )
        )

    # await bot.set_chat_menu_button(
    #     chat_id=message.chat.id,
    #     menu_button=MenuButtonWebApp(
    #         text="Open Menu",
    #         web_app=WebAppInfo(url=f"{application_settings.APP_HOSTNAME}/menu/"),
    #     ),
    # )

    sticker = FSInputFile("static/buddha.webp")
    await message.answer_sticker(
        sticker=sticker,
    )
    await message.answer(
        text=text,
        reply_markup=markup,
    )


@commands_router.message(Command(commands=["check"]))
async def check(message: Message, bot: Bot) -> None:
    task = send_message_task.apply_async(args=[message.from_user.id])

    await message.answer(
        text="Ok",
    )


# def get_string(tg_id: int, practice: str, event: str) -> str:
    # return f"{tg_id}_{practice}_{event}"

# RedisConnector.set(
#     key=get_string(tg_id=134154141, practice="asana", event="timer_paused"),
#     value=False,
# )

# value = RedisConnector.get(key=get_string(tg_id=134154141, practice="asana", event="timer_paused"))