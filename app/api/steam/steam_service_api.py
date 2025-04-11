from app.api.steam.get_schema_for_game.api import GetSchemaForGameApi
from app.api.steam.get_schema_for_game.responses import GetSchemaForGameResponse
from app.api.steam.owned_games.responses import GetOwnedGamesResponse
from app.api.steam.owned_games.api import GetOwnedGamesApi
from app.api.steam.player_achievements.api import GetPlayerAchievements
from app.api.steam.player_achievements.responses import GetPlayerAchievementsResponse


class SteamServiceApi:
    @staticmethod
    def get_owned_games() -> GetOwnedGamesResponse | None:
        return GetOwnedGamesApi.get_owned_games()

    @staticmethod
    def get_schema_for_game(appid: int) -> GetSchemaForGameResponse | None:
        return GetSchemaForGameApi.get_schema_for_game(appid)

    @staticmethod
    def get_player_achievements(appid: int) -> GetPlayerAchievementsResponse | None:
        return GetPlayerAchievements.get_player_achievements(appid)
