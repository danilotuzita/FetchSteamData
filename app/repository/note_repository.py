from sqlalchemy.orm import Session

from app.domain import Note
from app.repository import DatabaseService


class NoteRepository():
    @staticmethod
    def put_note(note: Note):
        with Session(DatabaseService.engine, expire_on_commit=False) as session:
            note.note_session_id = DatabaseService.get_current_operation_id()
            session.add(note)
            session.commit()
            return note
