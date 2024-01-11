import datetime
import uuid
from typing import Annotated, List

from pydantic import field_validator, Field, condecimal
from pydantic_core.core_schema import FieldValidationInfo

from src.core.schemas import APIModel, PaginatedAPIModel


class TransactionBase(APIModel):
    amount: Annotated[  # type: ignore
        condecimal(decimal_places=2),
        Field(
            ...,
            gt=0,
            description="Amount must be greater than 0",
        ),
    ]

    source_account_iban: str

    target_account_iban: str
    target_bic: str

    reference: str
    recipient_name: str

    @field_validator("target_account_iban")
    def validate_different_source_and_target(
        cls, v: str, info: FieldValidationInfo
    ) -> str:
        if "source_account_iban" in info.data and v == info.data["source_account_iban"]:
            raise ValueError("Source and target accounts must be different")
        return v


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: uuid.UUID

    created_at: datetime.datetime


class PaginatedTransactions(PaginatedAPIModel):
    transactions: List[Transaction]
