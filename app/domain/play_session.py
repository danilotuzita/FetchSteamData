from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.domain.base import Base
from app.domain.game import Game
from app.domain.operation_sequence import OperationSequence


class PlaySession(Base):
    __tablename__ = 'play_session'

    session_id: Mapped[int] = mapped_column(ForeignKey(OperationSequence.operation_id), primary_key=True)
    appid: Mapped[int] = mapped_column(ForeignKey(Game.appid), primary_key=True)
    minutes_played: Mapped[int]
    session_time: Mapped[int]
    play_count: Mapped[int] = mapped_column(default=1)
    fetch_time: Mapped[DateTime] = mapped_column(DateTime(), server_default=func.now())

    def __repr__(self) -> str:
        return f"PlaySession(session_id={self.session_id!r},appid={self.appid!r},name={self.game.name!r},total_minutes_played={self.game.total_minutes_played!r},minutes_played={self.minutes_played!r},session_time={self.session_time!r},play_count={self.play_count!r},session_fetch_time={self.fetch_time})"
