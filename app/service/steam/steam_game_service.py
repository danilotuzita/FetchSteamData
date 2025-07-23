import logging

from app.api.steam.owned_games.responses import GetOwnedGamesResponseGame
from app.api.steam.recently_played_games.responses import GetRecentlyPlayedGamesResponseGame
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
        recently_played_games = SteamServiceApi.get_recently_played_games()
        if not recently_played_games:
            logging.error("Failed to get recently played games from Steam API.")
            return []
        SteamGameService.check_recently_played_games(recently_played_games.games)
        return owned_games_response.games + [game.to_owned_game_response_game() for game in recently_played_games.games]

    @staticmethod
    def check_owned_games(games: list[GetOwnedGamesResponseGame]):
        logging.info(f'Checking Owned Games... Total={len(games)}')
        for game_api in games:
            GameService.put_game(game_api.appid, game_api.name)

    @staticmethod
    def check_recently_played_games(recently_played_games: list[GetRecentlyPlayedGamesResponseGame]):
        if not recently_played_games:
            logging.error("Failed to get recently played games from Steam API.")
            return []
        logging.info(f'Checking Recently Played Games... Total={len(recently_played_games)}')
        for game in recently_played_games:
            GameService.put_shared_game(game.appid, game.name)
