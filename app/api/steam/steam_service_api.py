from app.api.steam.get_schema_for_game.api import GetSchemaForGameApi
from app.api.steam.get_schema_for_game.response import GetSchemaForGameResponse
from app.api.steam.owned_games.response import GetOwnedGamesResponse
from app.api.steam.owned_games.api import GetOwnedGamesApi
from app.api.steam.player_achievements.api import GetPlayerAchievements
from app.api.steam.player_achievements.response import GetPlayerAchievementsResponse


class SteamServiceApi:
    @staticmethod
    def get_owned_games() -> GetOwnedGamesResponse:
        return GetOwnedGamesApi.get_owned_games()

    @staticmethod
    def get_schema_for_game(appid: int) -> GetSchemaForGameResponse:
        return GetSchemaForGameApi.get_schema_for_game(appid)

    @staticmethod
    def get_player_achievements(appid: int) -> GetPlayerAchievementsResponse:
        return GetPlayerAchievements.get_player_achievements(appid)
