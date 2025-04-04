import logging
from app.api.opentaiko.api import GetTaikoPlaySession
from app.api.opentaiko.consts import OPEN_TAIKO_APP_ID, OPEN_TAIKO_GAME_NAME
from app.domain.game import Game
from app.domain.play_session import PlaySession
from app.repository.game_repository import GameRepository
from app.repository.play_session_repository import PlaySessionRepository
from app.service.note_service import NoteService
from app.service.steam_games_service import SteamGamesService


class OpenTaikoService:
    @staticmethod
    def fetch_session_from_log_and_save_to_db():
        game = GameRepository.get_game(OPEN_TAIKO_APP_ID)
        if not game:
            game = GameRepository.put_game(Game(
                appid=OPEN_TAIKO_APP_ID,
                name=OPEN_TAIKO_GAME_NAME,
                total_minutes_played=0
            ))

        taiko_session = GetTaikoPlaySession.get_play_session()
        if not taiko_session:
            logging.error(f"Error trying to parse Open Taiko log! Skipping session...")
            return

        if len(taiko_session.songs_played) == 0:
            logging.warning(f"No songs played! Skipping session...")
            return

        last_taiko_play_session = PlaySessionRepository.get_last_play_session(OPEN_TAIKO_APP_ID)
        taiko_session.end_time = taiko_session.end_time.replace(microsecond=0)
        minutes_played = round((taiko_session.end_time - taiko_session.start_time).total_seconds() / 60)
        session_time = round(taiko_session.end_time.timestamp())
        play_count = last_taiko_play_session.play_count + 1 if last_taiko_play_session else 1

        if last_taiko_play_session and last_taiko_play_session.session_time == session_time:
            logging.debug(f'Skipping Play Session for Game name="{game.name}", appid={game.appid}. No changes detected.')
            return

        logging.info(f'New Play Session for Game name="{game.name}", appid={game.appid}, minutes_played={minutes_played}, last_played="{taiko_session.end_time}", play_count={play_count}.')
        play_session = PlaySessionRepository.put_play_session(PlaySession(
            appid=game.appid,
            minutes_played=minutes_played,
            session_time=session_time,
            play_count=play_count
        ))
        SteamGamesService.update_game(
            appid=game.appid,
            last_played=session_time,
            total_minutes_played=game.total_minutes_played + minutes_played,
            total_play_count=play_session.play_count,
            last_session_id=play_session.session_id
        )

        note_content = f"{len(taiko_session.songs_played)} songs played: {taiko_session.songs_played}"
        NoteService.put_note(play_session, note_content)
