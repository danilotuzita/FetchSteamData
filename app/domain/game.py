from typing import Optional
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.domain.base import Base
from app.domain.operation_sequence import OperationSequence


class Game(Base):
    __tablename__ = 'game'

    appid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    last_played: Mapped[int] = mapped_column(default=0)
    total_minutes_played: Mapped[int] = mapped_column(default=0)
    total_play_count: Mapped[int] = mapped_column(default=0)
    last_session_id: Mapped[Optional[int]] = mapped_column(ForeignKey(OperationSequence.operation_id))
    fetch_time: Mapped[DateTime] = mapped_column(DateTime(), server_default=func.now(), onupdate=func.now())
    first_fetched: Mapped[DateTime] = mapped_column(DateTime(), server_default=func.now())
