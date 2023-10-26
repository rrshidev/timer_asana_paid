from aiogram.filters.callback_data import CallbackData


class PracticeTimerCallback(CallbackData, prefix="P"):
    action: str
    # task_id: str
