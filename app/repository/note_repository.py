from sqlalchemy.orm import Session
from sqlalchemy import select

from app.domain.note import Note
from app.repository.database_service import DatabaseService


class NoteRepository():
    @staticmethod
    def put_note(note: Note):
        with Session(DatabaseService.engine, expire_on_commit=False) as session:
            note.note_session_id = DatabaseService.get_current_operation_id()
            session.add(note)
            session.commit()
            return note

    @staticmethod
    def get_note(note_id: int):
        pass
