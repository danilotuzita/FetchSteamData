import logging
import requests
import urllib

from app.api.steam.consts import STEAM_API_KEY, STEAM_ID_64
from app.api.steam.player_achievements.responses import GetPlayerAchievementsResponse

logging.basicConfig(format="%(asctime)s - %(levelname)s : %(message)s", level=logging.DEBUG)


class GetPlayerAchievements():
    get_player_achievements_url = "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/"

    @staticmethod
    def get_player_achievements(appid: int) -> GetPlayerAchievementsResponse:
        try:
            response = requests.get(
                GetPlayerAchievements.get_player_achievements_url,
                urllib.parse.urlencode(
                    {
                        'key': STEAM_API_KEY,
                        'steamid': STEAM_ID_64,
                        'appid': appid
                    }
                )
            )
            response.raise_for_status()
            json = response.json()
            return GetPlayerAchievementsResponse(**json)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                logging.debug(f"No achievements found for appid={appid}")
                return None
            raise e
        except Exception:
            logging.exception(f"Error trying to fetch User Stats for Game.")
            return None
