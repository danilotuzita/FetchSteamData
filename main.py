import config
import logging

from app.repository import OperationSequenceHandler
from app.domain import OperationCode


def fetch():
    with OperationSequenceHandler(OperationCode.FETCH) as operation_sequence:
        try:
            from app.service import SteamService
            from app.service import OpenTaikoService
            SteamService.fetch_user_data_from_steam_api_and_save_to_db()
            OpenTaikoService.fetch_session_from_log_and_save_to_db()
        except Exception as e:
            logging.exception(f"Unexpected Error!!!")
            operation_sequence.set_exception(e)


def undo_last_session(appid: int):
    with OperationSequenceHandler(OperationCode.UNDO_LAST_SESSION, f"Undo Last Session appid={appid}") as operation_sequence:
        try:
            from app.service import SteamService
            SteamService.undo_last_play_session(appid)
        except Exception as e:
            logging.exception(f"Unexpected Error!!!")
            operation_sequence.set_exception(e)


def add_note():
    with OperationSequenceHandler(OperationCode.ADD_NOTE) as operation_sequence:
        try:
            from app.service import NoteService
            NoteService.make_note_interactive()
        except Exception as e:
            logging.exception(f"Unexpected Error!!!")
            operation_sequence.set_exception(e)


def manual():
    with OperationSequenceHandler(OperationCode.MANUAL_OPERATION, "Manual Operation") as operation_sequence:
        try:
            from app.service import SteamService
            from app.repository import GameRepository
            from app.service import SteamAchivementsService
            games = GameRepository.get_all_games()
            for game in games:
                SteamAchivementsService.unlock_achivements(game)
            SteamService.fetch_user_data_from_steam_api_and_save_to_db()
        except Exception as e:
            logging.exception(f"Unexpected Error!!!")
            operation_sequence.set_exception(e)


def development():
    with OperationSequenceHandler(OperationCode.DEVELOPMENT, "Open Taiko [WIP]") as operation_sequence:
        try:
            from app.service import OpenTaikoService
            OpenTaikoService.fetch_session_from_log_and_save_to_db()
        except Exception as e:
            logging.exception(f"Unexpected Error!!!")
            operation_sequence.set_exception(e)


if __name__ == "__main__":
    try:
        with open("banner.txt") as banner:
            logging.info(banner.read())
    except:
        logging.info("FetchSteamData")
    mode = OperationCode.FETCH
    match mode:
        case OperationCode.FETCH:
            fetch()
        case OperationCode.UNDO_LAST_SESSION:
            undo_last_session(1091500)
        case OperationCode.MANUAL_OPERATION:
            manual()
        case OperationCode.DEVELOPMENT:
            development()
