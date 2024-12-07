import logging
from app.api.steam.owned_games.response import GetOwnedGamesResponseGame
from app.api.steam.steam_service_api import SteamServiceApi
from app.domain.achievements import Achievement
from app.domain.play_history import PlayHistory
from app.domain.play_session import PlaySession
from app.repository.database_repository import DatabaseRepository
from app.util import TimeUtil


class SteamService:
    @staticmethod
    def fetch_user_data_from_steam_api_and_save_to_db():
        played_games = SteamService.get_played_games()

        logging.info(f"Making Play History")
        play_history: list[PlayHistory] = []
        for game in played_games:
            play_history.append(PlayHistory(**vars(game)))
            logging.debug(f"New PlayHistory={game}.")
        DatabaseRepository.put_game_history(play_history)

        logging.info(f"Making Play Sessions")
        for game in play_history:
            play_session = SteamService.make_play_session(game)
            if play_session:
                SteamAchivementsService.fetch_game_data_from_steam_api_and_save_to_db(play_session)

    @staticmethod
    def get_played_games() -> list[GetOwnedGamesResponseGame]:
        owned_games_response = SteamServiceApi.get_owned_games()
        return [game for game in owned_games_response.games if game.playtime_forever]

    @staticmethod
    def make_play_session(current: PlayHistory) -> PlaySession:
        last_play_session = DatabaseRepository.get_last_play_session(current.appid)
        if last_play_session and last_play_session.session_time >= current.rtime_last_played:
            logging.debug(f"Skipping Play Session for Game name={current.name}, appid={current.appid}. No changes detected.")
            return None
        minutes_played = current.playtime_forever - last_play_session.total_minutes_played if last_play_session else 0
        play_count = last_play_session.play_count + 1 if last_play_session else 1
        logging.info(f"New Play Session for Game name={current.name}, appid={current.appid}. Minutes Played={minutes_played}, Last Played={TimeUtil.unixtime_to_localtime_str(current.rtime_last_played)}, Play Count={play_count}.")

        new_play_session = PlaySession(appid=current.appid, name=current.name, total_minutes_played=current.playtime_forever, minutes_played=minutes_played, session_time=current.rtime_last_played, play_count=play_count)
        DatabaseRepository.put_play_session(new_play_session)
        return new_play_session


class SteamAchivementsService:
    @staticmethod
    def fetch_game_data_from_steam_api_and_save_to_db(play_session: PlaySession):
        user_stats = SteamServiceApi.get_user_stats_for_game(play_session.appid)
        if user_stats is None or user_stats.playerstats is None:
            logging.error(f"Failed to get User Stats for Game name={play_session.name}, appid={play_session.appid}. Skipping...")
            return

        SteamAchivementsService.make_achievements(play_session)
        for achievement in user_stats.playerstats.achievements:
            if achievement.achieved != 1:
                continue
            DatabaseRepository.set_achievement_completed(play_session.appid, achievement.name)

    @staticmethod
    def make_achievements(play_session: PlaySession):
        db_achievement_count = DatabaseRepository.get_app_achivements_count(play_session.appid)
        game_schema = SteamServiceApi.get_schema_for_game(play_session.appid)
        if game_schema is None or game_schema.game is None or game_schema.game.availableGameStats is None:
            logging.error(f"Failed to get Game Schema for Game name={play_session.name}, appid={play_session.appid}. Skipping...")
            return
        if db_achievement_count >= len(game_schema.game.availableGameStats.achievements):
            return

        logging.debug(f"Found new Achievements for Game name={play_session.name}, appid={play_session.appid}. DbCount={db_achievement_count}, SteamCount={len(game_schema.game.availableGameStats.achievements)}.")
        achievements: list[Achievement] = []
        for achievement in game_schema.game.availableGameStats.achievements:
            achievements.append(Achievement(appid=play_session.appid, name=achievement.name, game_name=play_session.name, display_name=achievement.displayName, description=achievement.description, hidden=achievement.hidden))
        DatabaseRepository.put_achievements(achievements)
