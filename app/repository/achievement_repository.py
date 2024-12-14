
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domain.achievement import Achievement
from app.repository.database_service import DatabaseService


class AchievementRepository():
    @staticmethod
    def put_achievements(achievements: list[Achievement]) -> list[Achievement]:
        DatabaseService.get_operation()
        with Session(DatabaseService.engine) as session:
            for achievement in achievements:
                session.merge(achievement)
            session.commit()
            session.expunge_all()
            return achievements

    @staticmethod
    def get_app_achivements_count(appid: int) -> int:
        DatabaseService.get_operation()
        with Session(DatabaseService.engine) as session:
            return session.query(func.count(Achievement.appid)).where(Achievement.appid == appid).scalar()

    @staticmethod
    def set_achievement_unlocked(appid: int, name: str, unlocked_time: int = -1) -> Achievement:
        DatabaseService.get_operation()
        with Session(DatabaseService.engine) as session:
            achievement: Achievement = session.scalar(
                select(Achievement)
                .where(Achievement.appid == appid)
                .where(func.upper(Achievement.name) == name.upper())
                .where(Achievement.session_id_unlocked.is_(None))
            )
            if achievement is None:
                return None
            achievement.session_id_unlocked = DatabaseService.current_operation_id
            achievement.time_unlocked = unlocked_time
            session.commit()
            session.expunge_all()
            return achievement
