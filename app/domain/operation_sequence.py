from typing import Optional
from sqlalchemy import DateTime, ForeignKey, String, func
import sqlalchemy
import sqlalchemy.event
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.domain import Base


class OperationCode(Base):
    __tablename__ = 'operation_code'

    operation_code: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str]

    FETCH = "FETCH"
    UNDO_LAST_SESSION = "UNDO_LAST_SESSION"
    ADD_NOTE = "ADD_NOTE"
    MANUAL_OPERATION = "MANUAL_OPERATION"
    DEVELOPMENT = "DEVELOPMENT"

    @staticmethod
    def insert_data(target, connection, **kw):
        connection.execute(target.insert(), [
            {
                "operation_code": OperationCode.FETCH,
                "description": "Fetch Steam Data"
            },
            {
                "operation_code": OperationCode.UNDO_LAST_SESSION,
                "description": "Undo last session for game"
            },
            {
                "operation_code": OperationCode.ADD_NOTE,
                "description": "Add note for session"
            },
            {
                "operation_code": OperationCode.MANUAL_OPERATION,
                "description": "Manual Operation to fix data"
            },
            {
                "operation_code": OperationCode.DEVELOPMENT,
                "description": "Code for running the app while developing/testing"
            },
        ])


class OperationStatus(Base):
    __tablename__ = 'operation_status'

    operation_status: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str]

    START = "START"
    END = "END"
    ERROR = "ERROR"

    @staticmethod
    def insert_data(target, connection, **kw):
        connection.execute(target.insert(), [
            {
                "operation_status": OperationStatus.START,
                "description": "Operation is running"
            },
            {
                "operation_status": OperationStatus.END,
                "description": "Operation finished successfully"
            },
            {
                "operation_status": OperationStatus.ERROR,
                "description": "Operation finished with error"
            }
        ])


sqlalchemy.event.listen(OperationCode.__table__, 'after_create', OperationCode.insert_data)
sqlalchemy.event.listen(OperationStatus.__table__, 'after_create', OperationStatus.insert_data)


class OperationSequence(Base):
    __tablename__ = 'operation_sequence'

    operation_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    operation_code: Mapped[str] = mapped_column(ForeignKey(OperationCode.operation_code))
    operation_status: Mapped[str] = mapped_column(ForeignKey(OperationStatus.operation_status))
    operation_message: Mapped[Optional[str]] = mapped_column(String(128))
    operation_start_time: Mapped[DateTime] = mapped_column(DateTime())
    operation_end_time: Mapped[Optional[DateTime]] = mapped_column(DateTime())

    def __repr__(self) -> str:
        return self.to_string(
            f"""
            OperationSequence(
                operation_id={self.operation_id!r},
                operation_code={self.operation_code!r},
                operation_status={self.operation_status!r},
                operation_message={self.operation_message!r},
                operation_start_time='{self.operation_start_time}',
                operation_end_time='{self.operation_end_time}'
            )
            """
        )
