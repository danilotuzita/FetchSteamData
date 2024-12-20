import config
import logging

from app.repository.operation_sequence_handler import OperationSequenceHandler
from app.service.steam_service import SteamService

if __name__ == "__main__":
    try:
        with open("banner.txt") as banner:
            logging.info(banner.read())
    except:
        logging.info("FetchSteamData")
    manual = False
    if not manual:
        with OperationSequenceHandler() as op:
            try:
                SteamService.fetch_user_data_from_steam_api_and_save_to_db()
            except Exception as e:
                logging.exception(f"Unexpected Error!!!")
                op.set_exception(e)
    else:
        from app.domain.operation_sequence import OperationCode
        with OperationSequenceHandler(OperationCode.MANUAL_OPERATION, "Update Achievements") as op:
            try:
                from app.repository.game_repository import GameRepository
                from app.service.steam_service import SteamAchivementsService
                games = GameRepository.get_all_games()
                for game in games:
                    SteamAchivementsService.unlock_achivements(game)
                # SteamService.fetch_user_data_from_steam_api_and_save_to_db()
            except Exception as e:
                logging.exception(f"Unexpected Error!!!")
                op.set_exception(e)
