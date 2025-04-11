import logging

from app.api.steam.steam_service_api import SteamServiceApi
from app.domain.achievement import Achievement
from app.domain.game import Game
from app.domain.play_session import PlaySession
from app.repository.achievement_repository import AchievementRepository
from app.repository.game_repository import GameRepository
from app.util import TimeUtil


class SteamAchivementService:
    @staticmethod
    def update_achivements(appid: int):
        game = GameRepository.get_game(appid)
        if not game:
            logging.error(f"Game not found! appid={appid}")
            return
        if SteamAchivementService._make_achievements(game):
            SteamAchivementService._unlock_achivements(game)

    @staticmethod
    def _unlock_achivements(game: Game):
        achievements = SteamServiceApi.get_player_achievements(game.appid)
        if not achievements or not achievements.playerstats or not achievements.playerstats.achievements:
            logging.error(f'Failed to get Unlocked date of achivements for Game name="{game.name}", appid={game.appid}. Skipping...')
            return
        for achievement in achievements.playerstats.achievements:
            if achievement.achieved != 1:
                continue
            updated_achievement = AchievementRepository.set_achievement_unlocked(game.appid, achievement.apiname, achievement.unlocktime)
            if updated_achievement and updated_achievement.time_unlocked:
                logging.info(f'New Achievement Unlocked for Game! name="{updated_achievement.game_name}", appid={updated_achievement.appid}, achievement="{updated_achievement.display_name}", unlocked_at="{TimeUtil.unixtime_to_localtime_str(updated_achievement.time_unlocked)}".')

    @staticmethod
    def _make_achievements(game: Game) -> bool:
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
        achievements = AchievementRepository.get_session_achievements(session.appid, session.session_id)
        for achievement in achievements:
            logging.warning(f'Locking {achievement}')
            AchievementRepository.lock_achievement(achievement.appid, achievement.name)
