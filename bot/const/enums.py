from enum import StrEnum


class Practices(StrEnum):
    ASANA = "asana"
    PRANAYAMA = "pranayama"
    MEDITATION = "meditation"


class TimerStatus(StrEnum):
    RUNNING = "🟢"
    PAUSED = "🟡"
    STOPPED = "🔴"
