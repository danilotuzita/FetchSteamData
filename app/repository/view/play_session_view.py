from dataclasses import dataclass
from typing import Any, Sequence
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.repository.database_service import DatabaseService


@dataclass
class PlaySessionView():
    session_id: int
    game_name: str
    appid: int
    session_time: str
    time_played: str
    play_count: int
    time_played_until_session: str
    total_time_played: str
    achievements_unlocked: str
    session_notes: str
    cover_art: str = ""


class PlaySessionViewRepository():
    view_query = open("db/view_play_sessions.sql", "r").read()

    @staticmethod
    def get_latest_play_sessions(offset: int = 0, limit: int = 10) -> Sequence[PlaySessionView]:
        with Session(DatabaseService.engine, expire_on_commit=False) as session:
            play_sessions: Sequence[Sequence[Any]] = session.execute(
                text(
                    PlaySessionViewRepository.view_query
                ),
                {
                    "ofs": offset,
                    "lim": limit
                }
            ).all()  # type: ignore

            return [
                PlaySessionView(
                    session_id=play_session[0],
                    game_name=play_session[1],
                    appid=play_session[2],
                    session_time=play_session[3],
                    time_played=play_session[4],
                    play_count=play_session[5],
                    time_played_until_session=play_session[6],
                    total_time_played=play_session[7],
                    achievements_unlocked=play_session[8],
                    session_notes=play_session[9],
                )
                for play_session in play_sessions
            ]
