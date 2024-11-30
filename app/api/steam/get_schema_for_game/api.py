import requests
import urllib
from app.api.steam.consts.consts import STEAM_API_KEY, STEAM_USER_ID
from app.api.steam.get_schema_for_game.response import GetSchemaForGameResponse


class GetSchemaForGameApi():
    get_schema_for_game_url = "https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/"

    @staticmethod
    def get_schema_for_game(appid: int) -> GetSchemaForGameResponse:
        response = requests.get(
            GetSchemaForGameApi.get_schema_for_game_url,
            urllib.parse.urlencode(
                {
                    'key': STEAM_API_KEY,
                    'steamid': STEAM_USER_ID,
                    'appid': appid
                }
            )
        )
        json = response.json()
        return GetSchemaForGameResponse(**json)
