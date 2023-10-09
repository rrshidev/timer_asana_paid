from __future__ import annotations

from typing import Optional

from .core.types import jsonb

from sqlalchemy.orm import Mapped

from .core import ORMModel, mixins


class UserPracticeModel(
    mixins.UserIDMixin, mixins.PracticeIDMixin, ORMModel,
):
    data: Mapped[Optional[jsonb]]
