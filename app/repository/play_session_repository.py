
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.domain.play_session import PlaySession
from app.repository.database_service import DatabaseService


class PlaySessionRepository():
    @staticmethod
    def get_last_play_session(appid: int) -> PlaySession:
        DatabaseService.get_operation()
        with Session(DatabaseService.engine) as session:
            return session.scalars(
                select(PlaySession)
                .where(PlaySession.appid == appid)
                .order_by(PlaySession.operation_id.desc())
            ).first()

    @staticmethod
    def put_play_session(play_session: PlaySession) -> PlaySession:
        operation_id = DatabaseService.get_operation()
        with Session(DatabaseService.engine) as session:
            play_session.operation_id = operation_id
            session.add(play_session)
            session.commit()
            session.expunge_all()
            return play_session
