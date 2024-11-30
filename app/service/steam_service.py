from doctest import UnexpectedException
from re import S
from sqlalchemy import DateTime
from app.api.steam.owned_games.response import GetOwnedGamesResponseGame
from app.api.steam.steam_service_api import SteamServiceApi
from app.domain.achievements import Achievements
from app.domain.play_history import PlayHistory
from app.domain.play_session import PlaySession
from app.repository.database_repository import DatabaseRepository
from app.util import TimeUtil


class SteamService:
    @staticmethod
    def fetch_game_data_from_steam_api_and_save_to_db():
        played_games: list[PlayHistory] = []
        for game in SteamService.get_played_games():
            played_games.append(PlayHistory(**vars(game)))
        DatabaseRepository.put_game_history(played_games)

    @staticmethod
    def get_played_games() -> list[GetOwnedGamesResponseGame]:
        owned_games_response = SteamServiceApi.get_owned_games()
        return [game for game in owned_games_response.games if game.playtime_forever]

    @staticmethod
    def fetch_game_data_from_steam_api_and_save_to_db():
        played_games = SteamService.get_played_games()

        for game in played_games:
            db_achievement_count = DatabaseRepository.get_app_achivements_count(game.appid)
            if db_achievement_count == 0:
                SteamService.make_achievements(game)

            game_stats = SteamServiceApi.get_user_stats_for_game(game.appid)
            print(game_stats)
            if game_stats is None or game_stats.playerstats is None:
                raise UnexpectedException("Failed to get Game Stats")

            for achievement in game_stats.playerstats.achievements:
                if achievement.achieved != 1:
                    continue
                DatabaseRepository.set_achievement_completed(game.appid, achievement.name)

    @staticmethod
    def make_achievements(game: GetOwnedGamesResponseGame):
        game_schema = SteamServiceApi.get_schema_for_game(game.appid)
        if game_schema is None or game_schema.game is None or game_schema.game.availableGameStats is None:
            raise UnexpectedException("Failed to get Game Schema")

        achievements: list[Achievements] = []
        for achievement in game_schema.game.availableGameStats.achievements:
            achievements.append(Achievements(appid=game.appid, name=achievement.name, game_name=game.name, display_name=achievement.displayName, description=achievement.description, hidden=achievement.hidden))
        DatabaseRepository.put_achievements(achievements)

    @staticmethod
    def do_things():
        previous = DatabaseRepository.get_game_history(7670, 1)
        current = DatabaseRepository.get_game_history(7670, 2)
        SteamService.make_play_session(previous, current)

    @staticmethod
    def make_play_session(previous: PlayHistory, current: PlayHistory) -> PlaySession:
        if previous.rtime_last_played >= current.rtime_last_played:
            return

        minutes_played = current.playtime_forever - previous.playtime_forever
        last_play_session = DatabaseRepository.get_last_play_session(current.appid)
        play_count = last_play_session.play_count if last_play_session else 0
        session_time = TimeUtil.unixtime_to_localtime(current.rtime_last_played)

        new_play_session = PlaySession(
            appid=current.appid,
            name=current.name,
            minutes_played=minutes_played,
            session_time=session_time,
            play_count=play_count + 1,
        )
        DatabaseRepository.put_play_session(new_play_session)
