from typing import Sequence
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.domain.play_session import PlaySession
from app.repository.database_service import DatabaseService


class PlaySessionRepository():
    @staticmethod
    def put_play_session(play_session: PlaySession) -> PlaySession:
        with Session(DatabaseService.engine, expire_on_commit=False) as session:
            play_session.session_id = DatabaseService.get_current_operation_id()
            session.add(play_session)
            session.commit()
            return play_session

    @staticmethod
    def get_last_play_session(appid: int) -> PlaySession | None:
        with Session(DatabaseService.engine, expire_on_commit=False) as session:
            return session.scalar(
                select(PlaySession)
                .where(PlaySession.appid == appid)
                .order_by(PlaySession.session_id.desc())
            )

    @staticmethod
    def get_play_session(session_id: int, appid: int) -> PlaySession | None:
        with Session(DatabaseService.engine, expire_on_commit=False) as session:
            return session.scalar(
                select(PlaySession)
                .where(PlaySession.session_id == session_id)
                .where(PlaySession.appid == appid)
            )

    @staticmethod
    def remove_play_session(play_session: PlaySession):
        with Session(DatabaseService.engine, expire_on_commit=False) as session:
            session.delete(play_session)
            session.commit()

    @staticmethod
    def get_play_sessions(appid: int, offset: int = 0, limit: int = 10) -> Sequence[PlaySession]:
        with Session(DatabaseService.engine, expire_on_commit=False) as session:
            return session.scalars(
                select(PlaySession)
                .where(PlaySession.appid == appid)
                .order_by(PlaySession.session_id.desc())
                .offset(offset)
                .limit(limit)
            ).all()
