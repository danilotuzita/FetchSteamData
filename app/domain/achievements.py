from typing import Optional
from sqlalchemy import DateTime, String
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.domain.base import Base
from app.util import TimeUtil


class Achievements(Base):
    __tablename__ = 'achievements'

    appid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), primary_key=True)
    game_name: Mapped[str] = mapped_column(String(128))
    display_name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(512))
    hidden: Mapped[int]
    session_id_unlocked: Mapped[Optional[str]]
    session_fetched_time: Mapped[DateTime] = mapped_column(DateTime(True), server_default=func.now())

    def __repr__(self) -> str:
        raise NotImplementedError()
