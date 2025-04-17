import logging

from app.api.steam.owned_games.responses import GetOwnedGamesResponseGame
from app.api.steam.steam_service_api import SteamServiceApi
from app.service.game_service import GameService


class SteamGameService:
    @staticmethod
    def update_owned_games() -> list[GetOwnedGamesResponseGame]:
        owned_games_response = SteamServiceApi.get_owned_games()
        if not owned_games_response:
            logging.error("Failed to get owned games from Steam API.")
            return []
        SteamGameService.check_owned_games(owned_games_response.games)
        return owned_games_response.games

    @staticmethod
    def check_owned_games(games: list[GetOwnedGamesResponseGame]):
        logging.info(f'Checking Owned Games... Total={len(games)}')
        for game_api in games:
            GameService.put_game(game_api.appid, game_api.name)
