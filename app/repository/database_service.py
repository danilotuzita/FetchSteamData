import contextlib
import datetime
from email import contentmanager
import time
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session

from app.domain.achievement import Achievement
from app.domain.base import Base
from app.domain.play_session import PlaySession
from app.domain.operation_sequence import OperationCode, OperationSequence, OperationStatus
from app.repository.consts import DATABASE_NAME


class DatabaseService:
    engine = create_engine(f"sqlite:///{DATABASE_NAME}")
    current_operation_id: int = -1
    operation_start_time: float

    @staticmethod
    def _start_new_operation(operation_code=OperationCode.FETCH) -> int:
        DatabaseService.operation_start_time = time.time()
        with Session(DatabaseService.engine, expire_on_commit=False) as session:
            Base.metadata.create_all(DatabaseService.engine)
            last_operation = session.scalar(select(OperationSequence))
            if last_operation:
                last_operation.operation_id += 1
            else:
                last_operation = OperationSequence(
                    operation_id=1,
                    operation_code=operation_code
                )
                session.add(last_operation)
            DatabaseService.current_operation_id = last_operation.operation_id
            session.commit()
        return DatabaseService.current_operation_id

    @staticmethod
    def _end_operation() -> int:
        with Session(DatabaseService.engine, expire_on_commit=False) as session:
            current_operation = session.scalar(
                select(OperationSequence)
                .where(OperationSequence.operation_id == DatabaseService.current_operation_id)
            )
            if not current_operation:
                return -1
            current_operation.execution_end_time = time.time() - DatabaseService.operation_start_time
            session.commit()

    @staticmethod
    def get_operation() -> int:
        return DatabaseService.current_operation_id if DatabaseService.current_operation_id else DatabaseService._start_new_operation()


class Operation():
    def __init__(self, operation_code=OperationCode.FETCH) -> None:
        self.operation_code = operation_code

    def __enter__(self) -> "Operation":
        with Session(DatabaseService.engine) as session:
            Base.metadata.create_all(DatabaseService.engine)
            self.operation = OperationSequence(
                operation_code=self.operation_code,
                operation_status=OperationStatus.START
            )
            session.add(self.operation)
            session.commit()
        return self

    def error(self, exception: Exception):
        raise exception

    def __exit__(self, exception_type: type, exception_value: Exception, _exception_traceback):
        with Session(DatabaseService.engine):
            if exception_type:
                self.operation.operation_message = str(exception_value)
