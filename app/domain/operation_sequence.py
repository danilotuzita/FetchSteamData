from typing import Optional
from sqlalchemy import DateTime, ForeignKey, func
import sqlalchemy
import sqlalchemy.event
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.domain.base import Base


class OperationCode(Base):
    __tablename__ = 'operation_code'

    operation_code: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str]

    FETCH = "FETCH"

    @staticmethod
    def insert_data(target, connection, **kw):
        connection.execute(target.insert(), [
            OperationCode(
                operation_status=OperationCode.FETCH,
                description="Fetch Steam Data"
            )
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
            OperationStatus(
                operation_status=OperationStatus.START,
                description="Operation is running"
            ),
            OperationStatus(
                operation_status=OperationStatus.END,
                description="Operation finished sucessfully"
            ),
            OperationStatus(
                operation_status=OperationStatus.ERROR,
                description="Operation finished with error"
            )
        ])


sqlalchemy.event.listen(OperationCode.__table__, 'after_create', OperationCode.insert_data)
sqlalchemy.event.listen(OperationStatus.__table__, 'after_create', OperationStatus.insert_data)


class OperationSequence(Base):
    __tablename__ = 'operation_sequence'

    operation_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    operation_code: Mapped[str] = mapped_column(ForeignKey(OperationCode.operation_code))
    operation_status: Mapped[str] = mapped_column(ForeignKey(OperationStatus.operation_status))
    operation_message: Mapped[Optional[str]]
    operation_start_time: Mapped[DateTime] = mapped_column(server_default=func.now())
    execution_end_time: Mapped[Optional[DateTime]]
