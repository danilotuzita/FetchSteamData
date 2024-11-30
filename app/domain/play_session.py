import datetime
from sqlalchemy import DateTime, String
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.domain.base import Base
from app.util import TimeUtil


class PlaySession(Base):
    __tablename__ = 'play_session'

    session_id: Mapped[int] = mapped_column(primary_key=True)
    appid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    minutes_played: Mapped[int]
    session_time: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    play_count: Mapped[int] = mapped_column(default=1)
    session_fetched_time: Mapped[DateTime] = mapped_column(DateTime(True), server_default=func.now())

    def __repr__(self) -> str:
        raise NotImplementedError()
