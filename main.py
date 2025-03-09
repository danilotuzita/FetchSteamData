import config
import logging

from app.repository.operation_sequence_handler import OperationSequenceHandler
from app.service.steam_service import SteamService
from app.domain.operation_sequence import OperationCode


def fetch():
    with OperationSequenceHandler() as operation_sequence:
        try:
            SteamService.fetch_user_data_from_steam_api_and_save_to_db()
        except Exception as e:
            logging.exception(f"Unexpected Error!!!")
            operation_sequence.set_exception(e)


def undo_last_session(appid: int):
    with OperationSequenceHandler(OperationCode.UNDO_LAST_SESSION, f"Undo Last Session appid={appid}") as operation_sequence:
        try:
            SteamService.undo_last_play_session(appid)
        except Exception as e:
            logging.exception(f"Unexpected Error!!!")
            operation_sequence.set_exception(e)


def manual():
    with OperationSequenceHandler(OperationCode.MANUAL_OPERATION, "Manual Operation") as operation_sequence:
        try:
            from app.repository.game_repository import GameRepository
            from app.service.steam_achivements_service import SteamAchivementsService
            games = GameRepository.get_all_games()
            for game in games:
                SteamAchivementsService.unlock_achivements(game)
            SteamService.fetch_user_data_from_steam_api_and_save_to_db()
        except Exception as e:
            logging.exception(f"Unexpected Error!!!")
            operation_sequence.set_exception(e)


def development():
    with OperationSequenceHandler(OperationCode.DEVELOPMENT, "Notes [WIP]") as operation_sequence:
        try:
            from app.service.note_service import NoteService
            NoteService.make_note_interactive()
        except Exception as e:
            logging.exception(f"Unexpected Error!!!")
            operation_sequence.set_exception(e)


if __name__ == "__main__":
    try:
        with open("banner.txt") as banner:
            logging.info(banner.read())
    except:
        logging.info("FetchSteamData")
    mode = OperationCode.DEVELOPMENT
    match mode:
        case OperationCode.FETCH:
            fetch()
        case OperationCode.UNDO_LAST_SESSION:
            undo_last_session(1091500)
        case OperationCode.MANUAL_OPERATION:
            manual()
        case OperationCode.DEVELOPMENT:
            development()
