from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.domain import Base
from app.domain import Game
from app.domain import OperationSequence


class Note(Base):
    __tablename__ = 'note'

    note_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    note_session_id: Mapped[int] = mapped_column(ForeignKey(OperationSequence.operation_id))
    session_id: Mapped[int] = mapped_column(ForeignKey(OperationSequence.operation_id))
    appid: Mapped[int] = mapped_column(ForeignKey(Game.appid))
    content: Mapped[str] = mapped_column(String(512))
    create_time: Mapped[DateTime] = mapped_column(DateTime(), server_default=func.now())
    update_time: Mapped[DateTime] = mapped_column(DateTime(), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return self.to_string(
            f"""
            Note(
                note_id={self.note_id!r},
                note_session_id={self.session_id!r},
                session_id={self.session_id!r},
                appid={self.appid!r},
                content={self.content!r},
                create_time='{self.create_time}',
                update_time='{self.update_time}'
            )
            """
        )
