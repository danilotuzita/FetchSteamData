import logging
from typing import Sequence

from app.domain.play_session import PlaySession
from app.repository.game_repository import GameRepository
from app.repository.play_session_repository import PlaySessionRepository
from app.repository.view.play_session_view import PlaySessionView, PlaySessionViewRepository
from app.service.game_service import GameService
from app.service.steam.steam_achivement_service import SteamAchivementService
from app.util import TimeUtil


class PlaySessionService():
    @staticmethod
    def make_play_session(appid: int, current_last_played: int, current_playtime_forever: int) -> PlaySession | None:
        game = GameRepository.get_game(appid)
        if not game:
            logging.error(f'Game not found for appid={appid}!!!')
            return None
        if game.last_played >= current_last_played or game.total_minutes_played >= current_playtime_forever:
            logging.debug(f'Skipping Play Session for Game name="{game.name}", appid={game.appid}. No changes detected.')
            return None
        minutes_played = current_playtime_forever - game.total_minutes_played
        play_count = game.total_play_count + 1
        logging.info(f'New Play Session for Game name="{game.name}", appid={game.appid}, minutes_played={minutes_played}, last_played="{TimeUtil.unixtime_to_localtime_str(current_last_played)}", play_count={play_count}.')

        play_session = PlaySessionRepository.put_play_session(
            PlaySession(appid=game.appid, minutes_played=minutes_played, session_time=current_last_played, play_count=play_count)
        )
        if play_session:
            if play_session.appid > 0:  # if Steam Game
                SteamAchivementService.update_achivements(appid)
            GameService.update_game(
                appid,
                current_last_played,
                current_playtime_forever,
                play_count,
                play_session.session_id
            )
        return play_session

    @staticmethod
    def undo_last_play_session(appid: int):
        game = GameRepository.get_game(appid)
        session = PlaySessionRepository.get_last_play_session(appid)
        if not game or not session:
            logging.error(f'Session or Game not found for appid={appid}! Skipping...')
            return
        logging.info(f'Undoing {session}!!!')
        # Update Game
        logging.warning(f'Game before {game}')
        GameService.update_game(appid, 0, game.total_minutes_played - session.minutes_played, game.total_play_count - 1, 0)
        game = GameRepository.get_game(appid)
        logging.warning(f'Game after {game}')

        # Lock Achievements
        SteamAchivementService.lock_achivements_of_session(session)
        logging.warning(f'Removing {session}')

        # Remove Session
        PlaySessionRepository.remove_play_session(session)
        logging.info(f'Session Undone')

    @staticmethod
    def get_latest_play_sessions(offset: int = 0, limit: int = 10) -> Sequence[PlaySessionView]:
        return PlaySessionViewRepository.get_latest_play_sessions(offset, limit)
