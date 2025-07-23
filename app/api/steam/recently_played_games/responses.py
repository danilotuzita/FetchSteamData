from app.api.steam import ResponseWrapper
from app.api.steam.owned_games.responses import GetOwnedGamesResponseGame
from app.util.TimeUtil import get_current_unixtime


class GetRecentlyPlayedGamesResponseGame:
    def __init__(self, appid: int, name: str, playtime_2weeks: int, playtime_forever: int, img_icon_url: str, playtime_windows_forever: int, playtime_mac_forever: int, playtime_linux_forever: int, playtime_deck_forever: int, **_ignore) -> None:
        self.appid = appid
        self.name = name
        self.playtime_2weeks = playtime_2weeks
        self.playtime_forever = playtime_forever
        self.img_icon_url = img_icon_url
        self.playtime_windows_forever = playtime_windows_forever
        self.playtime_mac_forever = playtime_mac_forever
        self.playtime_linux_forever = playtime_linux_forever
        self.playtime_deck_forever = playtime_deck_forever
        self.rtimelast_played = get_current_unixtime()

    def __repr__(self):
        return f'GetRecentlyPlayedGamesResponseGame(appid={self.appid}, name="{self.name}", playtime_forever={self.playtime_forever}, rtime_last_played={self.rtimelast_played})'

    def to_owned_game_response_game(self):
        return GetOwnedGamesResponseGame(
            appid=self.appid,
            name=self.name,
            playtime_forever=self.playtime_forever,
            rtime_last_played=self.rtimelast_played,
            playtime_windows_forever=self.playtime_windows_forever,
            playtime_mac_forever=self.playtime_mac_forever,
            playtime_linux_forever=self.playtime_linux_forever,
            playtime_deck_forever=self.playtime_deck_forever
        )


class GetRecentlyPlayedGamesResponse(ResponseWrapper):
    def init(self, games: list, total_count: int) -> None:
        self.games = [GetRecentlyPlayedGamesResponseGame(**game) for game in games]
        self.total_count = total_count
