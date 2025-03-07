import logging

from app.domain.note import Note
from app.repository.game_repository import GameRepository
from app.repository.note_repository import NoteRepository
from app.repository.play_session_repository import PlaySessionRepository
from app.util import TimeUtil


class NoteService:
    @staticmethod
    def make_note_to_last_play_session(appid: int):
        session = PlaySessionRepository.get_last_play_session(appid)
        NoteService.make_note(session.session_id, session.appid)

    @staticmethod
    def make_note(session_id: int, appid: int):
        session = PlaySessionRepository.get_play_session(session_id, appid)
        if (session == None):
            logging.error(f"Session does not exist. session_id={session_id}, appid={appid}")
        game = GameRepository.get_game(appid)
        logging.info(f"""Adding note for: Game="{game.name}", Time={TimeUtil.unixtime_to_localtime_str(session.session_time)}, Minutes Played={TimeUtil.minutes_to_hours(session.minutes_played)}""")
        content = input("Input your note: ")
        if (len(content.strip()) == 0):
            logging.info("Note empty! Not adding.")
            return
        note = Note(
            session_id=session_id,
            appid=appid,
            content=content
        )
        note = NoteRepository.put_note(note)
        logging.info(f"Note added: {note}")
