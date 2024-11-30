
class GetUserStatsForGameResponseAchievements():
    def __init__(self, name: str, achieved: int, **ignore) -> None:
        self.name = name
        self.achieved = achieved

    def __repr__(self) -> str:
        return f"GetUserStatsForGameResponseAchievements(name={self.name!r},achieved={self.achieved!r})"


class GetUserStatsForGameResponsePlayerStats():
    def __init__(self, steamID: str, gameName: str, achievements: list[GetUserStatsForGameResponseAchievements], **ignore) -> None:
        self.steamID = steamID
        self.gameName = gameName
        self.achievements: list[GetUserStatsForGameResponseAchievements] = []
        for achievement in achievements:
            self.achievements.append(GetUserStatsForGameResponseAchievements(**achievement))

    def __repr__(self) -> str:
        return f"GetUserStatsForGameResponsePlayerStats(steamID={self.steamID!r},gameName={self.gameName!r},achievements={self.achievements})"


class GetUserStatsForGameResponse():
    def __init__(self, playerstats: GetUserStatsForGameResponsePlayerStats, **ignore):
        self.playerstats = GetUserStatsForGameResponsePlayerStats(**playerstats)

    def __repr__(self) -> str:
        return f"GetUserStatsForGameResponse(playerstats={self.playerstats!r})"
