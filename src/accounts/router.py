from fastapi import APIRouter, Depends, Query

from src.accounts.dependencies import get_account_by_iban
from src.accounts.repository import get_accounts_repository, AccountsRepository
from src.accounts.schemas import Account, PaginatedAccounts

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
)


@router.get(
    path="/",
    response_model=PaginatedAccounts,
)
async def get_accounts(
    balance_gt: float | None = None,
    balance_lt: float | None = None,
    page_size: int = Query(10, ge=1),
    page: int = Query(1, ge=1),
    accounts_dao: AccountsRepository = Depends(get_accounts_repository),
) -> PaginatedAccounts:
    return await accounts_dao.get_accounts(
        balance_gt=balance_gt,
        balance_lt=balance_lt,
        page_size=page_size,
        page=page,
    )


@router.get(
    path="/{account_iban}/",
    response_model=Account,
)
async def get_account(
    account: Account = Depends(get_account_by_iban),
) -> Account:
    return account
