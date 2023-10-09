from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from .buttons import MainMenuButtons, ChoosePracticeButtons


def user_main_markup() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    
    builder.row(
        KeyboardButton(
            text=MainMenuButtons.PRACTICE_TYPE.value,
        ),
        KeyboardButton(
            text=MainMenuButtons.SETS.value,
        )
    )

    return builder.as_markup(resize_keyboard=True)


def choose_practice_markup() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(
            text=ChoosePracticeButtons.ASANA.value,
        ),
    )

    builder.row(
        KeyboardButton(
            text=ChoosePracticeButtons.PRANAYAMA.value,
        ),
    )

    builder.row(
        KeyboardButton(
            text=ChoosePracticeButtons.MEDITATION.value,
        ),
    )

    builder.row(
        KeyboardButton(
            text=ChoosePracticeButtons.BACK.value,
        ),
    )

    return builder.as_markup(resize_keyboard=True)
