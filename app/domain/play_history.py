from sqlalchemy import DateTime, String
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.domain.base import Base
from app.util import TimeUtil


class PlayHistory(Base):
    __tablename__ = 'play_history'

    session_id: Mapped[int] = mapped_column(primary_key=True)
    appid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    playtime_forever: Mapped[int]
    playtime_windows_forever: Mapped[int]
    playtime_mac_forever: Mapped[int]
    playtime_linux_forever: Mapped[int]
    playtime_deck_forever: Mapped[int]
    rtime_last_played: Mapped[int]
    session_fetched_time: Mapped[DateTime] = mapped_column(DateTime(True), server_default=func.now())

    def __repr__(self) -> str:
        return f"PlayHistory(session_id={self.session_id!r},appid={self.appid!r},name={self.name!r},playtime_forever={TimeUtil.minutes_to_hours(self.playtime_forever)},rtime_last_played={TimeUtil.unixtime_to_localtime_str(self.rtime_last_played)})"
