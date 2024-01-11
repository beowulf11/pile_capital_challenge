import datetime
import uuid
from decimal import Decimal
from typing import List

from src.core.schemas import APIModel, PaginatedAPIModel


class AccountBase(APIModel):
    id: uuid.UUID
    name: str
    country: str
    balance: float
    iban: str
    created_at: datetime.datetime


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    pass


class PaginatedAccounts(PaginatedAPIModel):
    balances_sum: Decimal
    accounts: List[Account]
