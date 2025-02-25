from aiogram import Router, Bot
from aiogram.types import Message, FSInputFile, MenuButtonWebApp, WebAppInfo
from aiogram.filters import Command, ExceptionMessageFilter

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from app.database.orm import UserModel
import bot.const.phrases as phrases
from bot import markups
from app.settings import application_settings
from bot.background_tasks import send_message_task
from bot.filters import ButtonFilter
from bot.buttons import ChoosePracticeButtons


commands_router = Router()


@commands_router.message(Command(commands=["start"]))
@commands_router.message(ButtonFilter(button=ChoosePracticeButtons.BACK))
async def start(message: Message, bot: Bot, session: AsyncSession) -> None:
    first_name = message.from_user.first_name
    markup = markups.user_main_markup()
    text = phrases.phrase_for_start_first_greeting(first_name=first_name)

    # sending image sticker
    sticker = FSInputFile("static/buddha.webp")
    await message.answer_sticker(sticker)

    # check if user exists
    user = (
        await session.execute(
            select(UserModel).where(UserModel.tg_id.__eq__(message.from_user.id))
        )
    ).scalar()

    # if not => create
    if not user:
        await session.execute(
            insert(UserModel).values(
                {
                    UserModel.first_name: first_name,
                    UserModel.tg_id: message.from_user.id,
                    UserModel.tg_username: message.from_user.username,
                    UserModel.is_admin: False,
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
