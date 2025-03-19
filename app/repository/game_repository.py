from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.game import Game
from app.repository.database_service import DatabaseService


class GameRepository():
    @staticmethod
    def get_game(appid: int) -> Game:
        with Session(DatabaseService.engine, expire_on_commit=False) as session:
            return session.scalar(
                select(Game)
                .where(Game.appid == appid)
            )

    @staticmethod
    def put_game(game: Game) -> Game:
        with Session(DatabaseService.engine, expire_on_commit=False) as session:
            session.merge(game)
            session.commit()
            return game

    @staticmethod
    def get_all_games() -> list[Game]:
        with Session(DatabaseService.engine) as session:
            return session.scalars(select(Game)).all()
