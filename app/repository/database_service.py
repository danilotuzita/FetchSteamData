from sqlalchemy import create_engine

from app.domain.base import Base
from app.repository.consts import DATABASE_NAME


class NoActiveOperationError(Exception):
    """
    Error thrown when there's no Active Operation.
    To start an Operation:
    ```
    with Operation(operation_code) as operation:
        << Your code here >>
    ```
    """


class DatabaseService:
    engine = create_engine(f"sqlite:///{DATABASE_NAME}")
    current_operation_id: int = -1

    @staticmethod
    def get_current_operation_id() -> int:
        if not DatabaseService.current_operation_id or DatabaseService.current_operation_id <= 0:
            raise NoActiveOperationError(f"Please Initialize an Operation before!!!")
        return DatabaseService.current_operation_id


from app.domain.operation_sequence import OperationCode, OperationSequence, OperationStatus  # noqa
from app.domain.game import Game  # noqa
from app.domain.play_session import PlaySession  # noqa
from app.domain.achievement import Achievement  # noqa
from app.domain.note import Note  # noqa
Base.metadata.create_all(DatabaseService.engine)
