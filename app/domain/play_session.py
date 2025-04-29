from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from app.domain import game
from app.domain.base import Base
from app.domain.game import Game
from app.domain.operation_sequence import OperationSequence
from app.util import TimeUtil


class PlaySession(Base):
    __tablename__ = 'play_session'

    session_id: Mapped[int] = mapped_column(ForeignKey(OperationSequence.operation_id), primary_key=True)
    appid: Mapped[int] = mapped_column(ForeignKey(Game.appid), primary_key=True)
    minutes_played: Mapped[int]
    session_time: Mapped[int]
    play_count: Mapped[int] = mapped_column(default=1)
    fetch_time: Mapped[DateTime] = mapped_column(DateTime(), server_default=func.now())

    game: Mapped[Game] = relationship("Game", back_populates="play_sessions")

    def __repr__(self) -> str:
        return self.to_string(
            f"""
            PlaySession(
                session_id={self.session_id!r},
                appid={self.appid!r},
                minutes_played={TimeUtil.minutes_to_hours(self.minutes_played)},
                session_time='{TimeUtil.unixtime_to_localtime_str(self.session_time)}',
                play_count={self.play_count!r},
                session_fetch_time='{self.fetch_time}'
            )
            """
        )
