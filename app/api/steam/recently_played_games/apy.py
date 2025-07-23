import logging
import requests

from app.api.steam.consts import STEAM_API_KEY, STEAM_ID_64
from app.api.steam.recently_played_games.responses import GetRecentlyPlayedGamesResponse


class GetRecentlyPlayedGamesApi:
    get_recently_played_games_url = "https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/"
    get_recently_played_games_param = {
        'key': STEAM_API_KEY,
        'steamid': STEAM_ID_64,
        'count': 10  # Adjust count as needed
    }

    @staticmethod
    def get_recently_played_games() -> GetRecentlyPlayedGamesResponse | None:
        try:
            response = requests.get(GetRecentlyPlayedGamesApi.get_recently_played_games_url, GetRecentlyPlayedGamesApi.get_recently_played_games_param)
            response.raise_for_status()
            json = response.json()
            return GetRecentlyPlayedGamesResponse(**json)
        except Exception:
            logging.exception("Error trying to fetch Recently Played Games.")
            return None
