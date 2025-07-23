import logging

from app.domain.game import Game
from app.repository.game_repository import GameRepository
from app.util import TimeUtil


class GameService():
    @staticmethod
    def update_game(appid: int, last_played: int, total_minutes_played: int, total_play_count: int, last_session_id: int):
        game_db = GameRepository.get_game(appid)
        if not game_db:
            logging.error(f'Game not found! appid={appid}.')
            return
        game_db.last_played = last_played
        game_db.total_minutes_played = total_minutes_played
        game_db.total_play_count = total_play_count
        game_db.last_session_id = last_session_id
        logging.debug(f'Updating Game name="{game_db.name}", appid={game_db.appid}, last_played="{TimeUtil.unixtime_to_localtime_str(game_db.last_played)}", total_minutes_played={game_db.total_minutes_played}, total_play_count={game_db.total_play_count}, last_session_id={game_db.last_session_id}.')
        GameRepository.put_game(game_db)

    @staticmethod
    def put_game(appid: int, name: str) -> Game | None:
        game = GameRepository.get_game(appid)
        if game and game.is_shared == False:
            logging.debug(f'Game already exists! Game={game}. Skipping...')
            return game
        logging.info(f'New Game found! name="{name}", appid={appid}.')
        return GameRepository.put_game(Game(
            appid=appid,
            name=name,
            is_shared=False
        ))

    @staticmethod
    def put_shared_game(appid: int, name: str) -> Game | None:
        game = GameRepository.get_game(appid)
        if game:
            logging.debug(f'Game already exists! Game={game}. Skipping...')
            return game
        logging.info(f'New Shared Game found! name="{name}", appid={appid}.')
        return GameRepository.put_game(Game(
            appid=appid,
            name=name,
            is_shared=True
        ))
