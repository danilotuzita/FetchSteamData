from typing import Optional
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from app.domain.base import Base
from app.domain.operation_sequence import OperationSequence
from app.util import TimeUtil


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
    is_shared: Mapped[bool] = mapped_column(default=False)

    play_sessions = relationship("PlaySession", back_populates="game")

    def __repr__(self):
        return self.to_string(
            f"""
            Game(
                appid={self.appid!r},
                name={self.name!r},
                last_played='{TimeUtil.unixtime_to_localtime_str(self.last_played)}',
                total_minutes_played={TimeUtil.minutes_to_hours(self.total_minutes_played)},
                total_play_count={self.total_play_count!r},
                last_session_id={self.last_session_id!r},
                fetch_time='{self.fetch_time}',
                first_fetched='{self.first_fetched}',
                owned={self.is_shared!r}
            )
            """
        )
