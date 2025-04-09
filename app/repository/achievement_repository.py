from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domain import Achievement
from app.repository import DatabaseService


class AchievementRepository():
    @staticmethod
    def put_achievements(achievements: list[Achievement]) -> list[Achievement]:
        with Session(DatabaseService.engine, expire_on_commit=False) as session:
            for achievement in achievements:
                session.merge(achievement)
            session.commit()
            return achievements

    @staticmethod
    def get_app_achivements_count(appid: int) -> int:
        with Session(DatabaseService.engine) as session:
            return session.query(func.count(Achievement.appid)).where(Achievement.appid == appid).scalar()

    @staticmethod
    def set_achievement_unlocked(appid: int, name: str, unlocked_time: int = -1) -> Achievement:
        with Session(DatabaseService.engine, expire_on_commit=False) as session:
            achievement: Achievement = session.scalar(
                select(Achievement)
                .where(Achievement.appid == appid)
                .where(func.upper(Achievement.name) == name.upper())
                .where(Achievement.session_id_unlocked.is_(None))
            )
            if achievement is None:
                return None
            achievement.session_id_unlocked = DatabaseService.get_current_operation_id()
            achievement.time_unlocked = unlocked_time
            session.commit()
            return achievement

    @staticmethod
    def get_session_achievements(appid: int, session_id: int) -> list[Achievement]:
        with Session(DatabaseService.engine, expire_on_commit=False) as session:
            return session.scalars(
                select(Achievement)
                .where(Achievement.appid == appid)
                .where(Achievement.session_id_unlocked == session_id)
            ).all()

    @staticmethod
    def lock_achievement(appid: int, name: str):
        with Session(DatabaseService.engine, expire_on_commit=False) as session:
            achievement: Achievement = session.scalar(
                select(Achievement)
                .where(Achievement.appid == appid)
                .where(func.upper(Achievement.name) == name.upper())
            )
            if achievement is None:
                return
            achievement.session_id_unlocked = None
            achievement.time_unlocked = None
            session.commit()
