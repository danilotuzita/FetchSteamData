from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session

from app.domain.achievement import Achievement
from app.domain.base import Base
from app.domain.play_history import PlayHistory
from app.domain.play_session import PlaySession
from app.domain.session_sequence import SessionSequence
from app.repository.consts import DATABASE_NAME


class DatabaseRepository:
    engine = create_engine(f"sqlite:///{DATABASE_NAME}")
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
    def put_game_history(play_history_list: list[PlayHistory]) -> list[PlayHistory]:
        DatabaseRepository.get_session()
        with Session(DatabaseRepository.engine, expire_on_commit=False) as session:
            for game in play_history_list:
                game.session_id = DatabaseRepository.current_session_id
                session.add(game)
            session.commit()
            session.expunge_all()
            return play_history_list

    @staticmethod
    def put_achievements(achievements: list[Achievement]) -> list[Achievement]:
        DatabaseRepository.get_session()
        with Session(DatabaseRepository.engine, expire_on_commit=False) as session:
            for achievement in achievements:
                session.merge(achievement)
            session.commit()
            session.expunge_all()
            return achievements

    @staticmethod
    def get_app_achivements_count(appid: int) -> int:
        DatabaseRepository.get_session()
        with Session(DatabaseRepository.engine) as session:
            return session.query(func.count(Achievement.appid)).where(Achievement.appid == appid).scalar()

    @staticmethod
    def set_achievement_unlocked(appid: int, name: str, unlocked_time: int = None) -> Achievement:
        DatabaseRepository.get_session()
        with Session(DatabaseRepository.engine, expire_on_commit=False) as session:
            achievement: Achievement = session.scalar(
                select(Achievement)
                .where(Achievement.appid == appid)
                .where(func.upper(Achievement.name) == name.upper())
                .where(Achievement.session_id_unlocked.is_(None))
            )
            if achievement is None:
                return None
            achievement.session_id_unlocked = DatabaseRepository.current_session_id
            achievement.time_unlocked = unlocked_time if unlocked_time else -1
            session.commit()
            session.expunge_all()
            return achievement

    @staticmethod
    def get_last_play_session(appid: int) -> PlaySession:
        DatabaseRepository.get_session()
        with Session(DatabaseRepository.engine, expire_on_commit=False) as session:
            return session.scalars(
                select(PlaySession)
                .where(PlaySession.appid == appid)
                .order_by(PlaySession.session_id.desc())
            ).first()

    @staticmethod
    def put_play_session(play_session: PlaySession) -> PlaySession:
        DatabaseRepository.get_session()
        with Session(DatabaseRepository.engine, expire_on_commit=False) as session:
            play_session.session_id = DatabaseRepository.current_session_id
            session.add(play_session)
            session.commit()
            session.expunge_all()
            return play_session
