from app.api.steam.get_schema_for_game.api import GetSchemaForGameApi
from app.api.steam.get_schema_for_game.response import GetSchemaForGameResponse
from app.api.steam.owned_games.response import GetOwnedGamesResponse
from app.api.steam.owned_games.api import GetOwnedGamesApi
from app.api.steam.user_stats_for_game.response import GetUserStatsForGameResponse
from app.api.steam.user_stats_for_game.api import GetUserStatsForGameApi


class SteamServiceApi:

    @staticmethod
    def get_owned_games() -> GetOwnedGamesResponse:
        return GetOwnedGamesApi.get_owned_games()

    @staticmethod
    def get_user_stats_for_game(appid: int) -> GetUserStatsForGameResponse:
        return GetUserStatsForGameApi.get_user_stats_for_game(appid)

    @staticmethod
    def get_schema_for_game(appid: int) -> GetSchemaForGameResponse:
        return GetSchemaForGameApi.get_schema_for_game(appid)

    @staticmethod
    def get_fake_data(no: int) -> GetOwnedGamesResponse:
        match no:
            case 0:
                return GetOwnedGamesApi.get_fake_data()
            case 1:
                return GetOwnedGamesApi.get_fake_data1()
            case 2:
                return GetOwnedGamesApi.get_fake_data2()
