from __future__ import annotations

from .core.types import str_50

from sqlalchemy.orm import Mapped

from .core import ORMModel


class PracticeModel(
    ORMModel,
):
    name: Mapped[str_50]
