import urllib

import requests

from app.api.steam.consts.consts import STEAM_API_KEY, STEAM_USER_ID
from app.api.steam.owned_games.response import GetOwnedGamesResponse


fake_data_1 = {
    "response": {
        "game_count": 1,
        "games": [
            {
                "appid": 7670,
                "name": "BioShock",
                "playtime_forever": 0,
                "playtime_windows_forever": 0,
                "playtime_mac_forever": 0,
                "playtime_linux_forever": 0,
                "playtime_deck_forever": 0,
                "rtime_last_played": 0
            }
        ]
    }
}
fake_data_2 = {
    "response": {
        "game_count": 1,
        "games": [
            {
                "appid": 7670,
                "name": "BioShock",
                "playtime_forever": 30,
                "playtime_windows_forever": 0,
                "playtime_mac_forever": 0,
                "playtime_linux_forever": 0,
                "playtime_deck_forever": 0,
                "rtime_last_played": 1728811941
            }
        ]
    }
}


ach = {
    "response": {
        "game_count": 4,
        "games": [
            {
                "appid": 730,
                "name": "Counter-Strike 2",
                "playtime_forever": 119609,
                "img_icon_url": "8dbc71957312bbd3baea65848b545be9eae2a355",
                "has_community_visible_stats": True,
                "playtime_windows_forever": 28142,
                "playtime_mac_forever": 0,
                "playtime_linux_forever": 0,
                "playtime_deck_forever": 0,
                "rtime_last_played": 1697066612,
                "content_descriptorids": [
                    2,
                    5
                ],
                "playtime_disconnected": 0
            }, {
                "appid": 206440,
                "name": "To the Moon",
                "playtime_forever": 253,
                "img_icon_url": "6e29eb4076a6253fdbccb987a2a21746d2df54d7",
                "has_community_visible_stats": True,
                "playtime_windows_forever": 1,
                "playtime_mac_forever": 0,
                "playtime_linux_forever": 0,
                "playtime_deck_forever": 0,
                "rtime_last_played": 1590265920,
                "playtime_disconnected": 0
            },
        ]
    }
}


class GetOwnedGamesApi():
    get_owned_games_url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    get_owned_games_param = urllib.parse.urlencode(
        {
            'key': STEAM_API_KEY,
            'steamid': STEAM_USER_ID,
            'include_appinfo': True,
            'include_played_free_games': True
        }
    )

    @staticmethod
    def get_owned_games() -> GetOwnedGamesResponse:
        response = requests.get(GetOwnedGamesApi.get_owned_games_url, GetOwnedGamesApi.get_owned_games_param)
        json = response.json()
        return GetOwnedGamesResponse(**json)

    @staticmethod
    def get_fake_data() -> GetOwnedGamesResponse:
        return GetOwnedGamesResponse(**ach)

    @staticmethod
    def get_fake_data1() -> GetOwnedGamesResponse:
        return GetOwnedGamesResponse(**fake_data_1)

    @staticmethod
    def get_fake_data2() -> GetOwnedGamesResponse:
        return GetOwnedGamesResponse(**fake_data_2)
