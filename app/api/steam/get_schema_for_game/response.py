
class GetSchemaForGameResponseGameAvailableGameStatsAchievements():
    def __init__(self, name: str, displayName: str, hidden: int, description: str = "", **ignore) -> None:
        self.name = name
        self.displayName = displayName
        self.hidden = hidden
        self.description = description


class GetSchemaForGameResponseGameAvailableGameStats():
    def __init__(self, achievements: list[GetSchemaForGameResponseGameAvailableGameStatsAchievements], **ignore) -> None:
        self.achievements: list[GetSchemaForGameResponseGameAvailableGameStatsAchievements] = []
        for achievement in achievements:
            self.achievements.append(GetSchemaForGameResponseGameAvailableGameStatsAchievements(**achievement))


class GetSchemaForGameResponseGame():
    def __init__(self, gameName: str, gameVersion: str, availableGameStats: GetSchemaForGameResponseGameAvailableGameStats, **ignore) -> None:
        self.gameName = gameName
        self.gameVersion = gameVersion
        self.availableGameStats = GetSchemaForGameResponseGameAvailableGameStats(**availableGameStats)


class GetSchemaForGameResponse():
    def __init__(self, game: GetSchemaForGameResponseGame) -> None:
        self.game = GetSchemaForGameResponseGame(**game)
