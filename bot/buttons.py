from enum import StrEnum


class MainMenuButtons(StrEnum):
    PRACTICE_TYPE = "Выбрать тип практики"
    SETS = "Готовые комплексы"


class ChoosePracticeButtons(StrEnum):
    ASANA = "Асана"
    PRANAYAMA = "Пранаяма"
    MEDITATION = "Медитация"
    BACK = "Назад"
