from app.util import TimeUtil


class GetPlayerAchievementsResponseAchievements():
    def __init__(self, apiname: str, achieved: int, unlocktime: int) -> None:
        self.apiname = apiname
        self.achieved = achieved
        self.unlocktime = unlocktime

    def __repr__(self) -> str:
        return f"GetPlayerAchievementsResponseAchievements(name={self.apiname!r},achieved={self.achieved!r},unlocktime='{TimeUtil.unixtime_to_localtime_str(self.unlocktime)}')"


class GetPlayerAchievementsResponsePlayerStats():
    def __init__(self, steamID: str, gameName: str, achievements: list[GetPlayerAchievementsResponseAchievements], **ignore) -> None:
        self.steamID = steamID
        self.gameName = gameName
        self.achievements: list[GetPlayerAchievementsResponseAchievements] = []
        for achievement in achievements:
            self.achievements.append(GetPlayerAchievementsResponseAchievements(**achievement))

    def __repr__(self) -> str:
        return f"GetPlayerAchievementsResponsePlayerStats(steamID={self.steamID!r},gameName={self.gameName!r},achievements={self.achievements})"


class GetPlayerAchievementsResponse():
    def __init__(self, playerstats: GetPlayerAchievementsResponsePlayerStats, **ignore):
        self.playerstats = GetPlayerAchievementsResponsePlayerStats(**playerstats)

    def __repr__(self) -> str:
        return f"GetPlayerAchievementsResponse(playerstats={self.playerstats!r})"
