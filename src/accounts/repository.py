import re
from typing import AsyncGenerator, List

from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.accounts.exceptions import (
    NoAccountsFound,
    AccountIbanAlreadyExists,
    AccountIdAlreadyExists,
)
from src.accounts.models import AccountModel
from src.accounts.schemas import AccountCreate, Account, PaginatedAccounts
from src.core.schemas import PaginationDataAPIModel
from src.db.session import get_db_session
from src.debug.exceptions import InvalidSeedData


async def get_accounts_repository(
    session_manager: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator["AccountsRepository", None]:
    async with session_manager as session:
        yield AccountsRepository(session)


class AccountsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_accounts(
        self,
        *,
        balance_gt: float | None = None,
        balance_lt: float | None = None,
        page_size: int = 10,
        page: int = 1,
    ) -> PaginatedAccounts:
        # Define the subquery for filtered accounts
        account_filter = [
            None if balance_gt is None else AccountModel.balance >= balance_gt,
            None if balance_lt is None else AccountModel.balance <= balance_lt,
        ]
        subquery = (
            select(AccountModel, func.count().over().label("TotalFilteredAccounts"))
            .where(*filter(lambda x: x is not None, account_filter))  # type: ignore
            .order_by(AccountModel.created_at)
            .subquery()
        )

        # Define the subquery for paginated accounts
        page_offset = (page - 1) * page_size
        subquery = select(subquery).limit(page_size).offset(page_offset).subquery()

        # Define the subquery for filtered and summed accounts
        subquery = select(
            subquery, func.sum(subquery.c.balance).over().label("TotalSumBalance")
        ).subquery()

        result = await self.db.execute(select(subquery))
        data = result.fetchall()

        if not data:
            raise NoAccountsFound(
                page=page,
                page_size=page_size,
                balance_gt=balance_gt,
                balance_lt=balance_lt,
            )

        balances_sum = data[0][-1]
        accounts_count = data[0][-2]
        accounts = [Account.model_validate(account) for account in data]

        return PaginatedAccounts(
            balances_sum=balances_sum,
            accounts=accounts,
            metadata=PaginationDataAPIModel(
                count=len(accounts),
                offset=page_offset,
                limit=page_size,
                total=accounts_count,
            ),
        )

    async def get_account_by_iban(self, account_iban: str) -> AccountModel | None:
        account_result = await self.db.execute(
            select(AccountModel).filter(AccountModel.iban == account_iban)
        )

        account = account_result.scalars().one_or_none()
        if account is None:
            return None
        return account

    async def import_accounts(self, accounts: List[AccountCreate]) -> None:
        try:
            account_models = [
                AccountModel(**account.model_dump()) for account in accounts
            ]

            self.db.add_all(account_models)
            await self.db.commit()
        except IntegrityError as e:
            error_info = str(e.orig)
            id_match = re.search(r"\(id\)=\(([0-9a-fA-F-]+)\)", error_info)
            if id_match:
                raise AccountIdAlreadyExists(id_match.group(1)) from e  # type: ignore
            iban_match = re.search(r"\(iban\)=\((\'?.+?\'?)\)", error_info)
            if iban_match:
                raise AccountIbanAlreadyExists(iban_match.group(1)) from e
            raise InvalidSeedData() from e
        except DBAPIError as e:
            raise InvalidSeedData() from e
