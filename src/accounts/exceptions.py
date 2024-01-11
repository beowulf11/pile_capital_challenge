import uuid

from src.core.schemas import APIException


class AccountNotFound(APIException):
    def __init__(self, account_id: uuid.UUID | str):
        super().__init__(status_code=404, detail=f"Account {account_id} not found")


class NoAccountsFound(APIException):
    def __init__(
        self,
        page: int,
        page_size: int,
        balance_gt: float | None,
        balance_lt: float | None,
    ):
        conditions = (
            balance_gt is None and f"balance_lt={balance_lt}",
            balance_lt is None and f"balance_gt={balance_gt}",
        )
        super().__init__(
            status_code=404,
            detail=f"No accounts found for page={page}, page_size={page_size} {' and '.join(filter(None, conditions))}",  # type: ignore
        )


class AccountIdAlreadyExists(APIException):
    def __init__(self, account_id: uuid.UUID):
        super().__init__(
            status_code=400, detail=f"Account with id {account_id} already exists"
        )


class AccountIbanAlreadyExists(APIException):
    def __init__(self, account_iban: str):
        super().__init__(
            status_code=400, detail=f"Account with iban {account_iban} already exists"
        )
