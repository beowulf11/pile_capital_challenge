import json
import uuid

from fastapi import APIRouter, UploadFile, File, Depends

from src.accounts.repository import get_accounts_repository, AccountsRepository
from src.accounts.schemas import AccountCreate
from src.debug.exceptions import InvalidIBAN
from src.debug.utils import is_iban_valid

router = APIRouter(prefix="/debug")


@router.post(path="/seed/")
async def seed(
    upload_file: UploadFile = File(...),
    accounts_repository: AccountsRepository = Depends(get_accounts_repository),
) -> dict[str, str]:
    with upload_file.file as f:
        contents = f.read()
        seed_data = json.loads(contents)["data"]

        for seed_account in seed_data:
            if is_iban_valid(seed_account["IBAN"]) is False:
                raise InvalidIBAN(seed_account["IBAN"])

        accounts = [
            AccountCreate(
                id=uuid.UUID(account["id"]),
                iban=account["IBAN"],
                name=account["name"],
                country=account["country"],
                created_at=account["createdAt"][:-1],
                balance=account["balances"]["available"]["value"],
            )
            for account in seed_data
        ]

        await accounts_repository.import_accounts(accounts)

    return {"message": f"Successfully uploaded {upload_file.filename}"}
