from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Mapped

from ..types import practice_id_fk_type
from ..constraints import practice_id_fk


class PracticeIDMixin:
    practice_id: Mapped[practice_id_fk_type] = practice_id_fk

