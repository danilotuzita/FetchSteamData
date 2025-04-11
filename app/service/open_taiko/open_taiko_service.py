import logging

from app.api.opentaiko.api import GetTaikoPlaySession
from app.api.opentaiko.consts import OPEN_TAIKO_APP_ID, OPEN_TAIKO_GAME_NAME
from app.domain.game import Game
from app.repository.game_repository import GameRepository
from app.service.note_service import NoteService
from app.service.play_session_service import PlaySessionService


class OpenTaikoService:
    @staticmethod
    def fetch_session_from_log_and_save_to_db():
        game = OpenTaikoService.get_game()
        taiko_session = GetTaikoPlaySession.get_play_session()
        if not taiko_session or not taiko_session.session_time:
            logging.error(f"Error trying to parse Open Taiko log! Skipping session...")
            return

        if len(taiko_session.songs_played) == 0 or not taiko_session.minutes_played:
            logging.warning(f"No songs played! Skipping session...")
            return

        play_session = PlaySessionService.make_play_session(
            appid=OPEN_TAIKO_APP_ID,
            current_last_played=taiko_session.session_time,
            current_playtime_forever=(game.total_minutes_played + taiko_session.minutes_played)
        )

        if play_session:
            note_content = f"{len(taiko_session.songs_played)} songs played: {taiko_session.songs_played}"
            NoteService.put_note(play_session.appid, play_session.session_id, note_content)

    @staticmethod
    def get_game() -> Game:
        game = GameRepository.get_game(OPEN_TAIKO_APP_ID)
        if not game:
            game = GameRepository.put_game(Game(
                appid=OPEN_TAIKO_APP_ID,
                name=OPEN_TAIKO_GAME_NAME,
                total_minutes_played=0
            ))
        return game
