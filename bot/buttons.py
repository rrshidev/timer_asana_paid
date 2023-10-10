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

class PracticeStopProcessButtons(StrEnum):
    PAUSE = "Пауза ⏸"
    STOP = "Остановить практику ⏹"

class PracticeContinueProcessButtons(StrEnum):
    RESUME = "Возобновить ▶"