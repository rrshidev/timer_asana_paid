from typing import Dict

from aiogram.types import Message
from celery.schedules import schedule
from redbeat import RedBeatSchedulerEntry

from app import logger
from app.celery_config import celery_app
from bot.const import enums


class Timer:
    def __init__(self) -> None:
        self.entries: Dict = {}
    
    def get_entry(self, entry_name: str) -> Dict:
        return self.entries.get(entry_name) or {}

    def set_entry(self, entry_name: str, message: Message) -> None:
        entry = RedBeatSchedulerEntry(
            name=entry_name,
            task="bot.background_tasks.periodic.meditation.timer",
            args=[entry_name],
            schedule=schedule(run_every=1),
            app=celery_app,
        )
        self.entries[entry_name] = dict(
            entry=entry,
            message=message,
        )
        entry.save()
        logger.info(f'Entry "{entry.name}" set!\n Status: {entry.due_at}')
    
    def remove_entry(self, entry_name: str) -> None:
        entry: RedBeatSchedulerEntry = self.entries.get(entry_name, {}).get("entry")
        entry.delete()
        logger.info(f'Entry "{entry_name}" removed!')
