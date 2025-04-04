import logging

from pick import Option, pick
from thefuzz import process

from app.domain.game import Game
from app.domain.note import Note
from app.domain.play_session import PlaySession
from app.repository.game_repository import GameRepository
from app.repository.note_repository import NoteRepository
from app.repository.play_session_repository import PlaySessionRepository
from app.util import TimeUtil


class NoteService:
    @staticmethod
    def make_note_interactive():
        game = NoteInteractiveService.pick_game()
        if not game:
            return
        session = NoteInteractiveService.pick_session(game)
        if not session:
            return
        NoteService.make_note(session)

    @staticmethod
    def make_note_to_last_play_session(appid: int):
        session = PlaySessionRepository.get_last_play_session(appid)
        NoteService.make_note(session.session_id, session.appid)

    @staticmethod
    def make_note(session: PlaySession):
        if not session:
            logging.error(f"Invalid session! {session}")
            return
        game = GameRepository.get_game(session.appid)
        if not game:
            logging.error(f"Invalid game! {game}")
            return
        logging.info(f"""Adding note for: Game="{game.name}", Time={TimeUtil.unixtime_to_localtime_str(session.session_time)}, Minutes Played={TimeUtil.minutes_to_hours(session.minutes_played)}""")
        content = input("Input your note: ")
        if (len(content.strip()) == 0):
            logging.info("Note empty! Not adding.")
            return
        NoteService.put_note(session, content)

    @staticmethod
    def put_note(session: PlaySession, content: str):
        note = Note(
            session_id=session.session_id,
            appid=session.appid,
            content=content
        )
        note = NoteRepository.put_note(note)
        logging.info(f"Note added: {note}")


class NoteInteractiveService():
    QUIT = Option(value=-1, label="Quit")
    TRY_AGAIN = Option(value=-2, label="Try another game")
    PREVIOUS_PAGE = Option(value=-3, label="Previous Page <<")
    NEXT_PAGE = Option(value=-4, label="Next Page >>")

    PICK_GAME_OPTIONS = [TRY_AGAIN, QUIT]
    PICK_SESSION_OPTIONS = [PREVIOUS_PAGE, NEXT_PAGE, QUIT]

    INDICATOR = ">>"
    PAGE_SIZE = 5

    @staticmethod
    def pick_game() -> Game:
        logging.info("Activating interactive Note creation!")
        all_games = {game: game.name for game in GameRepository.get_all_games()}
        while True:
            query = input("Name of the Game: ")
            logging.debug(f"Looking for '{query}' in game list...")
            result = {
                r[2]: r[0]  # 0=value, 1=score, 2=key
                for r in process.extractBests(
                    query,
                    all_games,
                    score_cutoff=50
                )
            }
            logging.debug(f"Games found={[result.values()]}")
            if not len(result):
                selection = NoteInteractiveService.pick(
                    NoteInteractiveService.PICK_GAME_OPTIONS,
                    "No Games found, try another game..."
                )
                if selection == NoteInteractiveService.TRY_AGAIN:
                    logging.debug("Trying another game...")
                    continue
                logging.info(f"Quitting note creation")
                return None

            select_options = [Option(value=game, label=name) for game, name in result.items()]
            select_options.extend(NoteInteractiveService.PICK_GAME_OPTIONS)

            selection = NoteInteractiveService.pick(
                select_options,
                "Select the Game to add a Note:"
            )

            if selection == NoteInteractiveService.TRY_AGAIN:
                logging.debug("Trying another game...")
                continue
            elif selection == NoteInteractiveService.QUIT:
                logging.info(f"Quitting note creation")
                return None
            logging.debug(f"Selected {selection.value}")
            return selection.value

    @staticmethod
    def pick_session(game: Game) -> PlaySession:
        offset = 0
        found_at_least_once = False
        while True:
            if offset <= 0:
                offset = 0
            sessions = PlaySessionRepository.get_play_sessions(game.appid, offset, NoteInteractiveService.PAGE_SIZE)
            if not len(sessions):
                if found_at_least_once:
                    logging.debug("Moving back to the first page.")
                    offset = 0
                    continue
                logging.error(f"Sessions not found for {game}!")
                return None
            found_at_least_once = True
            select_options = [Option(value=session, label=str(session)) for session in sessions]
            select_options.extend(NoteInteractiveService.PICK_SESSION_OPTIONS)

            selection = NoteInteractiveService.pick(
                select_options,
                "Select the session to add a Note:"
            )
            if selection == NoteInteractiveService.QUIT:
                logging.info("Quitting note creation")
                return None
            elif selection == NoteInteractiveService.PREVIOUS_PAGE:
                offset -= NoteInteractiveService.PAGE_SIZE
                logging.debug(f"Moving to previous page. offset={offset}")
                continue
            elif selection == NoteInteractiveService.NEXT_PAGE:
                logging.debug(f"Moving to next page. offset={offset}")
                offset += NoteInteractiveService.PAGE_SIZE
                continue
            logging.debug(f"Selected {selection.value}")
            return selection.value

    @staticmethod
    def pick(options, title) -> Option:
        return pick(
            options,
            title,
            indicator=NoteInteractiveService.INDICATOR
        )[0]
