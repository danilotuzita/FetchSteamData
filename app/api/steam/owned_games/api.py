import logging
import urllib
import requests

from app.api.steam.consts import STEAM_API_KEY, STEAM_ID_64
from app.api.steam.owned_games.responses import GetOwnedGamesResponse


class GetOwnedGamesApi():
    get_owned_games_url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    get_owned_games_param = urllib.parse.urlencode(
        {
            'key': STEAM_API_KEY,
            'steamid': STEAM_ID_64,
            'include_appinfo': True,
            'include_played_free_games': True
        }
    )

    @staticmethod
    def get_owned_games() -> GetOwnedGamesResponse:
        try:
            response = requests.get(GetOwnedGamesApi.get_owned_games_url, GetOwnedGamesApi.get_owned_games_param)
            response.raise_for_status()
            json = response.json()
            return GetOwnedGamesResponse(**json)
        except Exception:
            logging.exception(f"Error trying to fetch Owned Games.")
            return None
