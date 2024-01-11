import decimal
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import String, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models import ModelBase


class AccountModel(ModelBase):
    __tablename__ = "accounts"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, index=True, default=uuid.uuid4
    )
    iban: Mapped[str] = mapped_column(String(255), unique=True)

    name: Mapped[str]
    country: Mapped[str] = mapped_column(String(255))
    balance: Mapped[Decimal] = mapped_column(DECIMAL(20, 2), default=0)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
