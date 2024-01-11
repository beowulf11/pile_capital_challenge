import json
import uuid
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.accounts.models import AccountModel


async def seed_accounts_table(
    dbsession: AsyncSession,
):
    with open("tests/seed/accounts.json", "r") as f:
        accounts_data = json.loads(f.read())

    for account in accounts_data["data"]:
        dbsession.add(
            AccountModel(
                id=uuid.UUID(account["id"]),
                iban=account["IBAN"],
                name=account["name"],
                country=account["country"],
                created_at=datetime.fromisoformat(account["createdAt"][:-1]),
                balance=account["balances"]["available"]["value"],
            )
        )

    await dbsession.commit()
