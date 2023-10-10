from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup

from .buttons import MainMenuButtons, ChoosePracticeButtons, StepBackButtons, PracticeStopProcessButtons, PracticeContinueProcessButtons


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


def step_back_markup() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(
            text=StepBackButtons.STEPBACK.value,
        ),
    )
    builder.row(
        KeyboardButton(
            text=StepBackButtons.FULLBACK.value,
        ),
    )
    
    return builder.as_markup(resize_keyboard=True)


def practice_stop_process_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        KeyboardButton(
            text=PracticeStopProcessButtons.PAUSE.value,
        ),
    )
    builder.row(
        KeyboardButton(
            text=PracticeStopProcessButtons.STOP.value,
        ),
    )
    
    return builder.as_markup(resize_keyboard=True)

def practice_continue_process_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        KeyboardButton(
            text=PracticeContinueProcessButtons.RESUME0.value,
        ),
    )
    builder.row(
        KeyboardButton(
            text=PracticeStopProcessButtons.STOP.value,
        ),
    )
    
    return builder.as_markup(resize_keyboard=True)
