
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.operation_sequence import OperationSequence
from app.repository.database_service import DatabaseService


class OperationSequenceRepository():

    @staticmethod
    def get_last_operation(operation_code: str) -> OperationSequence:
        with Session(DatabaseService.engine) as session:
            last_operation = session.scalars(
                select(OperationSequence)
                .where(OperationSequence.operation_code == operation_code)
                .order_by(OperationSequence.operation_id.desc())
            ).first()
            session.expunge(last_operation)
            return last_operation

    @staticmethod
    def put_operation(operation: OperationSequence):
        with Session(DatabaseService.engine) as session:
            session.add(operation)
            session.commit()

    @staticmethod
    def get_next_operation_id() -> int:
        with Session(DatabaseService.engine) as session:
            last_operation = session.scalars(
                select(OperationSequence)
                .order_by(OperationSequence.operation_id.desc())
            ).first()
            if last_operation:
                return last_operation.operation_id + 1
            return 1
