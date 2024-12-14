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

    with OperationSequenceHandler() as op:
        try:
            SteamService.fetch_user_data_from_steam_api_and_save_to_db()
        except Exception as e:
            logging.exception(f"Unexpected Error!!!")
            op.set_exception(e)
