import uuid
from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.accounts.exceptions import AccountNotFound
from src.accounts.models import AccountModel
from src.core.utils import json_dumps
from src.core.schemas import PaginationDataAPIModel
from src.db.session import get_db_session
from src.transactions.exceptions import InsufficientTransactionFunds, NoTransactionFound
from src.transactions.models import (
    TransactionModel,
    TransferStatus,
    TransferFailReason,
    TransferLogModel,
)
from src.transactions.schemas import (TransactionCreate, PaginatedTransactions,
                                      Transaction)


async def get_transactions_repository(
    session_manager: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator["TransactionsRepository", None]:
    async with session_manager as session:
        yield TransactionsRepository(session)


class TransactionsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_transactions(
        self, *, page_size: int, page: int
    ) -> PaginatedTransactions:
        subquery = (
            select(TransactionModel, func.count().over().label("TotalTransactions"))
            .order_by(TransactionModel.created_at)
            .subquery()
        )

        # Define the subquery for paginated accounts
        page_offset = (page - 1) * page_size
        subquery = select(subquery).limit(page_size).offset(page_offset).subquery()

        result = await self.db.execute(select(subquery))
        data = result.fetchall()

        if not data:
            raise NoTransactionFound(
                page=page,
                page_size=page_size,
            )

        transactions_count = data[0].TotalTransactions
        transactions = [Transaction.model_validate(transaction) for transaction in data]

        return PaginatedTransactions(
            transactions=transactions,
            metadata=PaginationDataAPIModel(
                count=len(transactions),
                offset=page_offset,
                limit=page_size,
                total=transactions_count,
            ),
        )

    async def create_transaction(
        self,
        transaction: TransactionCreate,
    ) -> TransactionModel:
        accounts = (
            (
                await self.db.execute(
                    select(AccountModel)
                    .where(
                        AccountModel.iban.in_(
                            [
                                transaction.source_account_iban,
                                transaction.target_account_iban,
                            ]
                        )
                    )
                    .with_for_update()
                )
            )
            .scalars()
            .all()
        )

        try:
            source_account = next(
                account
                for account in accounts
                if account.iban == transaction.source_account_iban
            )
        except StopIteration:
            raise AccountNotFound(transaction.source_account_iban)
        try:
            target_account = next(
                account
                for account in accounts
                if account.iban == transaction.target_account_iban
            )
        except StopIteration:
            raise AccountNotFound(transaction.target_account_iban)

        if source_account.balance < transaction.amount:
            raise InsufficientTransactionFunds(
                transaction.source_account_iban,
                source_account.balance,
                transaction.amount,
            )

        transaction_model = TransactionModel(**transaction.model_dump())
        self.db.add(transaction_model)

        source_account.balance -= transaction.amount
        target_account.balance += transaction.amount

        await self.db.commit()
        await self.db.refresh(transaction_model)

        return transaction_model

    async def log_transfer(
        self,
        transaction_id: uuid.UUID | None,
        transaction: TransactionCreate,
        status: TransferStatus,
        fail_reason: TransferFailReason | None,
    ) -> None:
        transfer_log = TransferLogModel(
            transaction_id=transaction_id,
            transfer_status=status,
            transfer_fail_reason=fail_reason,
            transfer_request=json_dumps(transaction.model_dump()),
        )

        self.db.add(transfer_log)
        await self.db.commit()
