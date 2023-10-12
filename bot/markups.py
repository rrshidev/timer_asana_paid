from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from .buttons import (
    MainMenuButtons, 
    ChoosePracticeButtons, 
    StepBackButtons, 
    PracticeStopProcessButtons, 
    PracticeContinueProcessButtons,
)


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

def step_asana_count_back_markup() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(
            text=StepBackButtons.ASANACOUNTBACK.value,
        ),
    )
    builder.row(
        KeyboardButton(
            text=StepBackButtons.FULLBACK.value,
        ),
    )

    return builder.as_markup(resize_keyboard=True)

def step_asana_time_back_markup() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(
            text=StepBackButtons.ASANATIMEBACK.value,
        ),
    )
    builder.row(
        KeyboardButton(
            text=StepBackButtons.FULLBACK.value,
        ),
    )

    return builder.as_markup(resize_keyboard=True)

def step_asana_relax_back_markup() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(
            text=StepBackButtons.ASANARELAXBACK.value,
        ),
    )
    builder.row(
        KeyboardButton(
            text=StepBackButtons.FULLBACK.value,
        ),
    )

    return builder.as_markup(resize_keyboard=True)

def step_shavasana_back_markup() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(
            text=StepBackButtons.SHAVASANABACK.value,
        ),
    )
    builder.row(
        KeyboardButton(
            text=StepBackButtons.FULLBACK.value,
        ),
    )

    return builder.as_markup(resize_keyboard=True)



def step_prana_count_back_markup() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(
            text=StepBackButtons.PRANACOUNTBACK.value,
        ),
    )
    builder.row(
        KeyboardButton(
            text=StepBackButtons.FULLBACK.value,
        ),
    )

    return builder.as_markup(resize_keyboard=True)

def step_prana_time_back_markup() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(
            text=StepBackButtons.PRANATIMEBACK.value,
        ),
    )
    builder.row(
        KeyboardButton(
            text=StepBackButtons.FULLBACK.value,
        ),
    )

    return builder.as_markup(resize_keyboard=True)

def step_prana_reload_back_markup() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(
            text=StepBackButtons.PRANARELOADBACK.value,
        ),
    )
    builder.row(
        KeyboardButton(
            text=StepBackButtons.FULLBACK.value,
        ),
    )

    return builder.as_markup(resize_keyboard=True)

def step_prana_medit_back_markup() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(
            text=StepBackButtons.PRANAMEDITBACK.value,
        ),
    )
    builder.row(
        KeyboardButton(
            text=StepBackButtons.FULLBACK.value,
        ),
    )

    return builder.as_markup(resize_keyboard=True)


#InllineButtons ---->

def practice_stop_process_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=PracticeStopProcessButtons.PAUSE.value,
            callback_data="meditation_pause",
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=PracticeStopProcessButtons.STOP.value,
            callback_data="meditation_stop",
        ),
    )
    
    return builder.as_markup(resize_keyboard=True)

def practice_continue_process_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=PracticeContinueProcessButtons.RESUME.value,
            callback_data="meditation_resume",
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=PracticeStopProcessButtons.STOP.value,
            callback_data="meditation_stop",
        ),
    )
    
    return builder.as_markup(resize_keyboard=True)
