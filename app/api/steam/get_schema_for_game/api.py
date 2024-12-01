import logging
import requests
import urllib
from app.api.steam.consts.consts import STEAM_API_KEY, STEAM_USER_ID
from app.api.steam.get_schema_for_game.response import GetSchemaForGameResponse


class GetSchemaForGameApi():
    get_schema_for_game_url = "https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/"

    @staticmethod
    def get_schema_for_game(appid: int) -> GetSchemaForGameResponse:
        try:
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
            response.raise_for_status()
            json = response.json()
            return GetSchemaForGameResponse(**json)
        except Exception:
            logging.exception(f"Error trying to fetch Schema for Game.")
            return None
