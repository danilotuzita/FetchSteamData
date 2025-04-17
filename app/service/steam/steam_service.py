import logging

from app.service.steam.steam_game_service import SteamGameService
from app.service.play_session_service import PlaySessionService


class SteamService:
    @staticmethod
    def fetch_user_data_from_steam_api_and_save_to_db():
        owned_games = SteamGameService.update_owned_games()
        played_games = [game for game in owned_games if game.playtime_forever]

        logging.info(f'Making Play Sessions...')
        for game in played_games:
            PlaySessionService.make_play_session(
                appid=game.appid,
                current_last_played=game.rtime_last_played,
                current_playtime_forever=game.playtime_forever,
            )
