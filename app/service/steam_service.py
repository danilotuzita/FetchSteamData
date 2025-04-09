import logging

from app.api.steam.owned_games.responses import GetOwnedGamesResponseGame
from app.domain import PlaySession
from app.repository import GameRepository
from app.repository import PlaySessionRepository
from app.service import SteamAchivementsService
from app.service import SteamGamesService
from app.util import TimeUtil


class SteamService:
    @staticmethod
    def fetch_user_data_from_steam_api_and_save_to_db():
        owned_games = SteamGamesService.update_owned_games()
        played_games = [game for game in owned_games if game.playtime_forever]

        logging.info(f'Making Play Sessions...')
        for game in played_games:
            play_session = SteamService.make_play_session(game)
            if play_session:
                SteamAchivementsService.update_achivements(game)
                SteamGamesService.update_game(
                    game.appid,
                    game.rtime_last_played,
                    game.playtime_forever,
                    play_session.play_count,
                    play_session.session_id
                )

    @staticmethod
    def make_play_session(game_api: GetOwnedGamesResponseGame) -> PlaySession:
        game_db = GameRepository.get_game(game_api.appid)
        if game_db and game_db.last_played >= game_api.rtime_last_played:
            logging.debug(f'Skipping Play Session for Game name="{game_api.name}", appid={game_api.appid}. No changes detected.')
            return None
        minutes_played = game_api.playtime_forever - (game_db.total_minutes_played if game_db else 0)
        play_count = game_db.total_play_count + 1 if game_db else 1
        logging.info(f'New Play Session for Game name="{game_api.name}", appid={game_api.appid}, minutes_played={minutes_played}, last_played="{TimeUtil.unixtime_to_localtime_str(game_api.rtime_last_played)}", play_count={play_count}.')

        new_play_session = PlaySession(appid=game_api.appid, minutes_played=minutes_played, session_time=game_api.rtime_last_played, play_count=play_count)
        PlaySessionRepository.put_play_session(new_play_session)
        return new_play_session

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
        SteamGamesService.update_game(appid, 0, game.total_minutes_played - session.minutes_played, game.total_play_count - 1, 0)
        game = GameRepository.get_game(appid)
        logging.warning(f'Game after {game}')

        # Lock Achievements
        SteamAchivementsService.lock_achivements_of_session(session)
        logging.warning(f'Removing {session}')

        # Remove Session
        PlaySessionRepository.remove_play_session(session)
        logging.info(f'Session Undone')
