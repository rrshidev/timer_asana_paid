from aiogram import Router, types, F
from sqlalchemy.ext.asyncio import AsyncSession


messages_router = Router()


# using magic filters
@messages_router.message(F.is_("lol"))
async def start(message: types.Message, session: AsyncSession) -> None:
    await message.answer(
        text="lmao"
    )


@messages_router.message(F.contains("yes"))
async def start(message: types.Message, session: AsyncSession) -> None:
    await message.answer(
        text="Of course!"
    )


@messages_router.message()
async def start(message: types.Message, session: AsyncSession) -> None:
    await message.answer(
        text=message.text
    )
