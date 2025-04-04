import logging

from app.api.steam.owned_games.responses import GetOwnedGamesResponseGame
from app.api.steam.steam_service_api import SteamServiceApi
from app.domain.game import Game
from app.repository.game_repository import GameRepository
from app.util import TimeUtil


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
