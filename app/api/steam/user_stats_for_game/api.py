import logging
import requests
import urllib
from app.api.steam.consts.consts import STEAM_API_KEY, STEAM_USER_ID
from app.api.steam.user_stats_for_game.response import GetUserStatsForGameResponse

logging.basicConfig(format="%(asctime)s - %(levelname)s : %(message)s", level=logging.DEBUG)


class GetUserStatsForGameApi():
    get_user_stats_for_game_url = "https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/"

    @staticmethod
    def get_user_stats_for_game(appid: int) -> GetUserStatsForGameResponse:
        try:
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
            response.raise_for_status()
            json = response.json()
            return GetUserStatsForGameResponse(**json)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                logging.debug(f"No achievements found for appid={appid}")
                return None
            raise e
        except Exception:
            logging.exception(f"Error trying to fetch User Stats for Game.")
            return None
