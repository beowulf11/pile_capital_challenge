from fastapi import Depends, HTTPException

from src.accounts.repository import get_accounts_repository, AccountsRepository
from src.accounts.schemas import Account


async def get_account_by_iban(
    account_iban: str,
    accounts_dao: AccountsRepository = Depends(get_accounts_repository),
) -> Account:
    account = await accounts_dao.get_account_by_iban(account_iban=account_iban)
    if account is None:
        raise HTTPException(
            status_code=404, detail=f"Account with IBAN {account_iban} not found"
        )

    return Account.model_validate(account)
