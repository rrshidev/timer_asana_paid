from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Mapped

from ..types import user_id_fk_type
from ..constraints import user_id_fk


class UserIDMixin:
    user_id: Mapped[user_id_fk_type] = user_id_fk
