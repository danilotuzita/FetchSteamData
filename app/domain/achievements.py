from typing import Optional
from sqlalchemy import DateTime, String
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.domain.base import Base
from app.util import TimeUtil


class Achievement(Base):
    __tablename__ = 'achievement'

    appid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), primary_key=True)
    game_name: Mapped[str] = mapped_column(String(128))
    display_name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(512))
    hidden: Mapped[int]
    session_id_unlocked: Mapped[Optional[int]]
    session_fetched_time: Mapped[DateTime] = mapped_column(DateTime(True), server_default=func.now())

    def __repr__(self) -> str:
        return f"Achievement(appid={self.appid!r},name={self.name!r},game_name={self.game_name!r},display_name={self.display_name!r},description={self.description!r},hidden={self.hidden!r},session_id_unlocked={self.session_id_unlocked!r},session_fetched_time={TimeUtil.unixtime_to_localtime_str(self.session_fetched_time)})"
