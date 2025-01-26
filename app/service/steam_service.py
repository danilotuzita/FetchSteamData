import logging

from app.api.steam.owned_games.response import GetOwnedGamesResponseGame
from app.api.steam.steam_service_api import SteamServiceApi
from app.domain.achievement import Achievement
from app.domain.game import Game
from app.domain.play_session import PlaySession
from app.repository.achievement_repository import AchievementRepository
from app.repository.game_repository import GameRepository
from app.repository.play_session_repository import PlaySessionRepository
from app.util import TimeUtil


class SteamService:
    @staticmethod
    def fetch_user_data_from_steam_api_and_save_to_db():
        owned_games = SteamGamesService.update_owned_games()
        played_games = [game for game in owned_games if game.playtime_forever]

        logging.info(f'Making Play Sessions...')
        for game in played_games:
            play_session = SteamService.make_play_session(game)
            if play_session:
                SteamAchivementsService.update_achivements(game)
                SteamGamesService.update_game(
                    game.appid,
                    game.rtime_last_played,
                    game.playtime_forever,
                    play_session.play_count,
                    play_session.session_id
                )

    @staticmethod
    def make_play_session(game_api: GetOwnedGamesResponseGame) -> PlaySession:
        game_db = GameRepository.get_game(game_api.appid)
        if game_db and game_db.last_played >= game_api.rtime_last_played:
            logging.debug(f'Skipping Play Session for Game name="{game_api.name}", appid={game_api.appid}. No changes detected.')
            return None
        minutes_played = game_api.playtime_forever - (game_db.total_minutes_played if game_db else 0)
        play_count = game_db.total_play_count + 1 if game_db else 1
        logging.info(f'New Play Session for Game name="{game_api.name}", appid={game_api.appid}, minutes_played={minutes_played}, last_played="{TimeUtil.unixtime_to_localtime_str(game_api.rtime_last_played)}", play_count={play_count}.')

        new_play_session = PlaySession(appid=game_api.appid, minutes_played=minutes_played, session_time=game_api.rtime_last_played, play_count=play_count)
        PlaySessionRepository.put_play_session(new_play_session)
        return new_play_session

    @staticmethod
    def undo_play_session(appid: int):
        game = GameRepository.get_game(appid)
        session = PlaySessionRepository.get_last_play_session(appid)
        if not game or not session:
            logging.error(f'Session or Game not found for appid={appid}! Skipping...')
            return
        logging.info(f'Undoing {session}!!!')
        # Update Game
        logging.warning(f'Game before {game}')
        SteamGamesService.update_game(appid, 0, game.total_minutes_played - session.minutes_played, game.total_play_count - 1, 0)
        game = GameRepository.get_game(appid)
        logging.warning(f'Game after {game}')

        # Lock Achievements
        SteamAchivementsService.lock_achivements_of_session(session)
        logging.warning(f'Removing {session}')

        # Remove Session
        PlaySessionRepository.remove_play_session(session)
        logging.info(f'Session Undone')


class SteamAchivementsService:
    @staticmethod
    def update_achivements(game: Game):
        if SteamAchivementsService.make_achievements(game):
            SteamAchivementsService.unlock_achivements(game)

    @staticmethod
    def unlock_achivements(game: Game):
        achievements = SteamServiceApi.get_player_achievements(game.appid)
        if not achievements or not achievements.playerstats or not achievements.playerstats.achievements:
            logging.error(f'Failed to get Unlocked date of achivements for Game name="{game.name}", appid={game.appid}. Skipping...')
            return
        for achievement in achievements.playerstats.achievements:
            if achievement.achieved != 1:
                continue
            updated_achievement = AchievementRepository.set_achievement_unlocked(game.appid, achievement.apiname, achievement.unlocktime)
            if updated_achievement:
                logging.info(f'New Achievement Unlocked for Game! name="{updated_achievement.game_name}", appid={updated_achievement.appid}, achievement="{updated_achievement.display_name}", unlocked_at="{TimeUtil.unixtime_to_localtime_str(updated_achievement.time_unlocked)}".')

    @staticmethod
    def make_achievements(game: Game) -> bool:
        db_achievement_count = AchievementRepository.get_app_achivements_count(game.appid)
        game_schema = SteamServiceApi.get_schema_for_game(game.appid)
        if game_schema is None or game_schema.game is None or game_schema.game.availableGameStats is None:
            logging.error(f'Failed to get Game Schema for Game name="{game.name}", appid={game.appid}. Skipping...')
            return False
        if db_achievement_count >= len(game_schema.game.availableGameStats.achievements):
            return True

        logging.info(f'Found new Achievements for Game name="{game.name}", appid={game.appid}. db_count={db_achievement_count}, steam_count={len(game_schema.game.availableGameStats.achievements)}.')
        achievements: list[Achievement] = []
        for achievement in game_schema.game.availableGameStats.achievements:
            achievements.append(Achievement(appid=game.appid, name=achievement.name, game_name=game.name, display_name=achievement.displayName, description=achievement.description, hidden=achievement.hidden))
        AchievementRepository.put_achievements(achievements)
        return True

    @staticmethod
    def lock_achivements_of_session(session: PlaySession):
        logging.warning(f'Locking achievements of {session}')
        achievements: list[Achievement] = AchievementRepository.get_session_achievements(session.appid, session.session_id)
        for achievement in achievements:
            logging.warning(f'Locking {achievement}')
            AchievementRepository.lock_achievement(achievement.appid, achievement.name)


class SteamGamesService:
    @staticmethod
    def update_owned_games() -> list[GetOwnedGamesResponseGame]:
        owned_games_response = SteamServiceApi.get_owned_games()
        SteamGamesService.check_owned_games(owned_games_response.games)
        return owned_games_response.games

    @staticmethod
    def check_owned_games(games: list[GetOwnedGamesResponseGame]):
        logging.info(f'Checking Owned Games... Total={len(games)}')
        for game_api in games:
            if GameRepository.get_game(game_api.appid):
                logging.debug(f'Skipping Owned Game name="{game_api.name}", appid={game_api.appid}. Game already exists in DB.')
                continue
            GameRepository.put_game(Game(
                appid=game_api.appid,
                name=game_api.name
            ))
            logging.info(f'New Owned Game found! name="{game_api.name}", appid={game_api.appid}, total_minutes_played={game_api.playtime_forever}.')

    @staticmethod
    def update_game(appid: int, last_played: int, total_minutes_played: int, total_play_count: int, last_session_id: int):
        game_db = GameRepository.get_game(appid)
        game_db.last_played = last_played
        game_db.total_minutes_played = total_minutes_played
        game_db.total_play_count = total_play_count
        game_db.last_session_id = last_session_id
        logging.debug(f'Updating Owned Game name="{game_db.name}", appid={game_db.appid}, last_played="{TimeUtil.unixtime_to_localtime_str(game_db.last_played)}", total_minutes_played={game_db.total_minutes_played}, total_play_count={game_db.total_play_count}, last_session_id={game_db.last_session_id}.')
        GameRepository.put_game(game_db)
