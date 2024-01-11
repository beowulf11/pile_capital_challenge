from decimal import Decimal

from src.core.schemas import APIException


class InsufficientTransactionFunds(APIException):
    def __init__(self, source_iban: str, balance: Decimal, amount: Decimal):
        super().__init__(
            status_code=400,
            detail=f"Transaction from {source_iban} failed due to insufficient funds. Balance: {balance}, Amount: {amount}",
        )


class NoTransactionFound(APIException):
    def __init__(
        self,
        page: int,
        page_size: int,
    ):
        super().__init__(
            status_code=404,
            detail=f"No transactions found for page {page} and page size {page_size}",
        )
