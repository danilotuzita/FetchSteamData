import datetime
import logging
from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.operation_sequence import OperationCode, OperationSequence, OperationStatus
from app.repository.database_service import DatabaseService


class OperationSequenceHandler():
    def __init__(self, operation_code=OperationCode.FETCH, message: Optional[str] = None) -> None:
        self.operation_code = operation_code
        self.exception: Optional[Exception] = None
        self.message: Optional[str] = message

    def __enter__(self) -> "OperationSequenceHandler":
        with Session(DatabaseService.engine) as session:
            operation = OperationSequence(
                operation_code=self.operation_code,
                operation_status=OperationStatus.START,
                operation_start_time=datetime.datetime.now(datetime.UTC),
                operation_message=self.message
            )
            session.add(operation)
            session.commit()
            DatabaseService.current_operation_id = operation.operation_id
            logging.debug(f"Start OperationSequence={operation}")
        return self

    def set_exception(self, exception: Exception):
        self.exception = exception

    def __exit__(self, exception_type: type, exception_value: Exception, traceback):
        with Session(DatabaseService.engine) as session:
            operation = session.scalar(
                select(OperationSequence)
                .where(OperationSequence.operation_id == DatabaseService.current_operation_id)
            )
            operation.operation_end_time = datetime.datetime.now(datetime.UTC)  # type: ignore
            if self.exception or exception_type:
                operation.operation_status = OperationStatus.ERROR  # type: ignore
                operation.operation_message = str(self.exception or exception_value)  # type: ignore
            else:
                operation.operation_status = OperationStatus.END
            session.commit()
            DatabaseService.current_operation_id = -1
            logging.debug(f"Ended OperationSequence={operation}")
