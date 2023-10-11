from enum import StrEnum


class MainMenuButtons(StrEnum):
    PRACTICE_TYPE = "Выбрать тип практики"
    SETS = "Готовые комплексы"


class ChoosePracticeButtons(StrEnum):
    ASANA = "🤸‍♀️ Асана 🤸‍♂️"
    PRANAYAMA = "🙏 Пранаяма 🙏"
    MEDITATION = "🧘 Медитация 🧘🏼‍♂️"
    BACK = "🔙 Назад"

class StepBackButtons(StrEnum):
    STEPBACK = "Вернуться к предыдущему шагу 🔙"
    FULLBACK = "Вернуться к выбору практики"
    
    ASANACOUNTBACK = "Вернуться к предыдущему шагу 👈"
    ASANATIMEBACK = "Вернуться к предыдущему шагу 👆"
    ASANARELAXBACK = "Вернуться к предыдущему шагу 👇"
    SHAVASANABACK = "Вернуться к предыдущему шагу 🎒"

    PRANACOUNTBACK = "Вернуться к предыдущему шагу 🤚"
    PRANATIMEBACK = "Вернуться к предыдущему шагу 👉"
    PRANARELOADBACK = "Вернуться к предыдущему шагу 🥾"
    PRANAMEDITBACK = "Вернуться к предыдущему шагу 📛"

class PracticeStopProcessButtons(StrEnum):
    PAUSE = "Пауза ⏸"
    STOP = "Остановить практику ⏹"

class PracticeContinueProcessButtons(StrEnum):
    RESUME = "Возобновить ▶"