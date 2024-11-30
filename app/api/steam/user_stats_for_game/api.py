import requests
import urllib
from app.api.steam.consts.consts import STEAM_API_KEY, STEAM_USER_ID
from app.api.steam.user_stats_for_game.response import GetUserStatsForGameResponse


class GetUserStatsForGameApi():
    get_user_stats_for_game_url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/"

    @staticmethod
    def get_user_stats_for_game(appid: int) -> GetUserStatsForGameResponse:
        response = requests.get(
            GetUserStatsForGameApi.get_user_stats_for_game_url,
            urllib.parse.urlencode(
                {
                    'key': STEAM_API_KEY,
                    'steamid': STEAM_USER_ID,
                    'appid': appid
                }
            )
        )
        json = response.json()
        return GetUserStatsForGameResponse(**json)
