from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.domain.base import Base


class SessionSequence(Base):
    __tablename__ = 'session_sequence'

    session_id: Mapped[int] = mapped_column(primary_key=True)
