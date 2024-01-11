import uuid

from src.accounts.exceptions import AccountNotFound
from src.transactions.exceptions import InsufficientTransactionFunds
from src.transactions.models import TransferStatus, TransferFailReason
from src.transactions.repository import TransactionsRepository
from src.transactions.schemas import TransactionCreate


async def log_success_transfer(
    transaction_id: uuid.UUID,
    transaction: TransactionCreate,
    transactions_repo: TransactionsRepository,
) -> None:
    await transactions_repo.log_transfer(
        transaction_id=transaction_id,
        transaction=transaction,
        status=TransferStatus.SUCCESS,
        fail_reason=None,
    )


async def log_error_transfer(
    exception: Exception,
    transaction_create: TransactionCreate,
    transactions_repo: TransactionsRepository,
) -> None:
    if isinstance(exception, InsufficientTransactionFunds):
        await transactions_repo.log_transfer(
            transaction_id=None,
            transaction=transaction_create,
            status=TransferStatus.FAILED,
            fail_reason=TransferFailReason.INSUFFICIENT_FUNDS,
        )
    elif isinstance(exception, AccountNotFound):
        await transactions_repo.log_transfer(
            transaction_id=None,
            transaction=transaction_create,
            status=TransferStatus.FAILED,
            fail_reason=TransferFailReason.INVALID_ACCOUNT,
        )
    else:
        await transactions_repo.log_transfer(
            transaction_id=None,
            transaction=transaction_create,
            status=TransferStatus.FAILED,
            fail_reason=TransferFailReason.UNKNOWN,
        )
