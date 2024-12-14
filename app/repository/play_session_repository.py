
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.domain.play_session import PlaySession
from app.repository.database_service import DatabaseService


class PlaySessionRepository():
    @staticmethod
    def get_last_play_session(appid: int) -> PlaySession:
        with Session(DatabaseService.engine, expire_on_commit=False) as session:
            play_session = session.scalars(
                select(PlaySession)
                .where(PlaySession.appid == appid)
                .order_by(PlaySession.session_id.desc())
            ).first()
            return play_session

    @staticmethod
    def put_play_session(play_session: PlaySession) -> PlaySession:
        with Session(DatabaseService.engine, expire_on_commit=False) as session:
            play_session.session_id = DatabaseService.get_current_operation_id()
            session.add(play_session)
            session.commit()
            return play_session
