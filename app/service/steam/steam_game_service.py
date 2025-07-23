import logging

from app.api.steam.owned_games.responses import GetOwnedGamesResponseGame
from app.api.steam.recently_played_games.responses import GetRecentlyPlayedGamesResponseGame
from app.api.steam.steam_service_api import SteamServiceApi
from app.service.game_service import GameService


class SteamGameService:
    @staticmethod
    def update_owned_games() -> list[GetOwnedGamesResponseGame]:
        return SteamGameService.check_owned_games() + SteamGameService.check_recently_played_games()

    @staticmethod
    def check_owned_games() -> list[GetOwnedGamesResponseGame]:
        owned_games_response = SteamServiceApi.get_owned_games()
        if owned_games_response is None:
            logging.error("Failed to get owned games from Steam API.")
            return []
        logging.info(f'Checking Owned Games... Total={len(owned_games_response.games)}')
        for game_api in owned_games_response.games:
            GameService.put_game(game_api.appid, game_api.name)
        return owned_games_response.games

    @staticmethod
    def check_recently_played_games() -> list[GetOwnedGamesResponseGame]:
        recently_played_games_response = SteamServiceApi.get_recently_played_games()
        if recently_played_games_response is None:
            logging.error("Failed to get recently played games from Steam API.")
            return []
        logging.info(f'Checking Recently Played Games... Total={len(recently_played_games_response.games)}')
        for game in recently_played_games_response.games:
            GameService.put_shared_game(game.appid, game.name)
        return [game.to_owned_game_response_game() for game in recently_played_games_response.games]
