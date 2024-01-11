import decimal
import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import ForeignKey, DECIMAL, JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models import ModelBase


class TransactionModel(ModelBase):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, index=True, default=uuid.uuid4
    )

    amount: Mapped[Decimal] = mapped_column(DECIMAL(20, 2))

    source_account_iban: Mapped[str] = mapped_column(
        ForeignKey("accounts.iban"),
        index=True,
    )

    target_account_iban: Mapped[str] = mapped_column(
        ForeignKey("accounts.iban"),
        index=True,
    )
    target_bic: Mapped[str]

    reference: Mapped[str]
    recipient_name: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class TransferStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"


class TransferFailReason(str, Enum):
    INSUFFICIENT_FUNDS = "insufficient_funds"
    INVALID_ACCOUNT = "invalid_account"
    UNKNOWN = "unknown"


class TransferLogModel(ModelBase):
    __tablename__ = "transfer_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, index=True, default=uuid.uuid4
    )

    transaction_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("transactions.id"),
    )
    transfer_status: Mapped[TransferStatus]
    transfer_fail_reason: Mapped[TransferFailReason | None]
    transfer_request: Mapped[str] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
