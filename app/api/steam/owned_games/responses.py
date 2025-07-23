from app.api.steam import ResponseWrapper
from app.util import TimeUtil


class GetOwnedGamesResponseGame:
    def __init__(self, appid: int, name: str, playtime_forever: int, rtime_last_played: int, playtime_windows_forever: int, playtime_mac_forever: int, playtime_linux_forever: int, playtime_deck_forever: int, **_ignore) -> None:
        self.appid = appid
        self.name = name
        self.playtime_forever = playtime_forever
        self.playtime_windows_forever = playtime_windows_forever
        self.playtime_mac_forever = playtime_mac_forever
        self.playtime_linux_forever = playtime_linux_forever
        self.playtime_deck_forever = playtime_deck_forever
        self.rtime_last_played = rtime_last_played

    def __repr__(self) -> str:
        return f"GetOwnedGamesResponseGame(appid={self.appid!r},name={self.name!r},playtime_forever={TimeUtil.minutes_to_hours(self.playtime_forever)},rtime_last_played={TimeUtil.unixtime_to_localtime_str(self.rtime_last_played)})"


class GetOwnedGamesResponse(ResponseWrapper):
    def init(self, game_count: int, games: list[GetOwnedGamesResponseGame]) -> None:
        self.game_count = game_count
        self.games: list[GetOwnedGamesResponseGame] = []
        for game in games:
            self.games.append(GetOwnedGamesResponseGame(**game))

    def __repr__(self) -> str:
        return f"GetOwnedGamesResponse(game_count={self.game_count!r},games={self.games})"
