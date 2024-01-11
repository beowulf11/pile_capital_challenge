from fastapi import APIRouter, Depends, Query

from src.transactions.models import TransactionModel
from src.transactions.repository import (get_transactions_repository,
                                         TransactionsRepository)
from src.transactions.schemas import (TransactionCreate, Transaction,
                                      PaginatedTransactions)
from src.transactions.utils import log_error_transfer, log_success_transfer

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
)


@router.get(
    path="/",
    response_model=PaginatedTransactions,
)
async def get_transactions(
    transactions_repo: TransactionsRepository = Depends(get_transactions_repository),
    page_size: int = Query(10, ge=1),
    page: int = Query(1, ge=1),
) -> PaginatedTransactions:
    return await transactions_repo.get_transactions(
        page_size=page_size,
        page=page,
    )


@router.post(
    path="/",
    status_code=201,
    response_model=Transaction,
)
async def create_transaction(
    transaction_create: TransactionCreate,
    transactions_repo: TransactionsRepository = Depends(get_transactions_repository),
) -> TransactionModel:
    try:
        data = await transactions_repo.create_transaction(transaction_create)
        await log_success_transfer(
            transaction_id=data.id,
            transaction=transaction_create,
            transactions_repo=transactions_repo,
        )
        return data
    except Exception as e:
        await log_error_transfer(
            exception=e,
            transaction_create=transaction_create,
            transactions_repo=transactions_repo,
        )
        raise e
