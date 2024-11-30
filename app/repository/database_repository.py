from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session

from app.domain.achievements import Achievements
from app.domain.base import Base
from app.domain.play_history import PlayHistory
from app.domain.play_session import PlaySession
from app.domain.session_sequence import SessionSequence


class DatabaseRepository:
    engine = create_engine("sqlite:///steam.db", echo=True)
    current_session_id: int = None

    @staticmethod
    def _start_new_session() -> int:
        with Session(DatabaseRepository.engine) as session:
            Base.metadata.create_all(DatabaseRepository.engine)
            last_session = session.scalar(select(SessionSequence))
            if last_session:
                last_session.session_id += 1
            else:
                last_session = SessionSequence(session_id=0)
                session.add(last_session)
            DatabaseRepository.current_session_id = last_session.session_id
            session.commit()
        return DatabaseRepository.current_session_id

    @staticmethod
    def get_session() -> int:
        return DatabaseRepository.current_session_id if DatabaseRepository.current_session_id else DatabaseRepository._start_new_session()

    @staticmethod
    def put_game_history(games: list[PlayHistory]):
        DatabaseRepository.get_session()
        with Session(DatabaseRepository.engine) as session:
            for game in games:
                game.session_id = DatabaseRepository.current_session_id
                session.add(game)
            session.commit()

    @staticmethod
    def get_last_game_history(appid: int) -> PlayHistory:
        DatabaseRepository.get_session()
        with Session(DatabaseRepository.engine) as session:
            return session.scalars(
                select(PlayHistory)
                .where(PlayHistory.appid == appid)
                .order_by(PlayHistory.session_id.desc())
            ).first()

    @staticmethod
    def get_game_history(appid: int, session_id: int) -> PlayHistory:
        DatabaseRepository.get_session()
        with Session(DatabaseRepository.engine) as session:
            return session.scalars(
                select(PlayHistory)
                .where(PlayHistory.appid == appid)
                .where(PlayHistory.session_id == session_id)
            ).first()

    @staticmethod
    def put_achievements(achievements: list[Achievements]):
        DatabaseRepository.get_session()
        with Session(DatabaseRepository.engine) as session:
            session.add_all(achievements)
            session.commit()

    @staticmethod
    def get_app_achivements_count(appid: int) -> int:
        DatabaseRepository.get_session()
        with Session(DatabaseRepository.engine) as session:
            return session.query(func.count(Achievements.appid)).where(Achievements.appid == appid).scalar()

    @staticmethod
    def set_achievement_completed(appid: int, name: str) -> int:
        DatabaseRepository.get_session()
        with Session(DatabaseRepository.engine) as session:
            achievement: Achievements = session.scalar(
                select(Achievements)
                .where(Achievements.appid == appid)
                .where(Achievements.name == name)
                .where(Achievements.session_id_unlocked.is_(None))
            )
            if achievement is None:
                return
            achievement.session_id_unlocked = DatabaseRepository.current_session_id
            session.commit()

    @staticmethod
    def get_last_play_session(appid: int) -> PlaySession:
        DatabaseRepository.get_session()
        with Session(DatabaseRepository.engine) as session:
            return session.scalars(
                select(PlaySession)
                .where(PlaySession.appid == appid)
                .order_by(PlaySession.session_id.desc())
            ).first()

    @staticmethod
    def put_play_session(play_session: PlaySession):
        DatabaseRepository.get_session()
        with Session(DatabaseRepository.engine) as session:
            play_session.session_id = DatabaseRepository.current_session_id
            session.add(play_session)
            session.commit()
