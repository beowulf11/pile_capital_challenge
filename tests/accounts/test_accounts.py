from decimal import Decimal
from typing import List, Tuple

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.accounts.models import AccountModel
from src.accounts.schemas import Account
from tests.seed.seed import seed_accounts_table


@pytest.mark.anyio
async def test_empty_db_accounts(
    client: AsyncClient,
    fastapi_app: FastAPI,
    dbsession: AsyncSession,
) -> None:
    url = fastapi_app.url_path_for("get_accounts")
    response = await client.get(url)

    assert response.status_code == 404


@pytest.mark.anyio
async def test_accounts_and_sum(
    client: AsyncClient,
    fastapi_app: FastAPI,
    dbsession: AsyncSession,
) -> None:
    await seed_accounts_table(dbsession)

    db_account_models = (
        (
            await dbsession.execute(
                select(AccountModel).order_by(AccountModel.created_at).limit(10).offset(0)
            )
        )
        .scalars()
        .all()
    )

    url = fastapi_app.url_path_for("get_accounts")
    response = await client.get(
        url,
        params={
            "page": 1,
            "page_size": 10,
        },
    )
    response_data = response.json()

    response_sum = Decimal(response_data["balancesSum"])
    response_accounts = [
        Account.model_validate(account) for account in response_data["accounts"]
    ]

    db_sum = sum([account.balance for account in db_account_models])
    db_accounts = [Account.model_validate(account) for account in db_account_models]

    assert response.status_code == 200
    assert response_sum == db_sum
    assert response_accounts == db_accounts


@pytest.mark.anyio
async def test_accounts_page_size(
    client: AsyncClient,
    fastapi_app: FastAPI,
    dbsession: AsyncSession,
) -> None:
    await seed_accounts_table(dbsession)

    conditions: List[Tuple[int, int]] = [
        (None, 12331),
        (None, None),
        (223, None),
        (12331, 123945),
        (1, 2),
    ]

    for greater_than_condition, less_then_condition in conditions:
        db_filters = []
        query_params = {}

        if greater_than_condition is not None:
            db_filters.append(AccountModel.balance >= greater_than_condition)
            query_params["balance_gt"] = greater_than_condition
        if less_then_condition is not None:
            db_filters.append(AccountModel.balance <= less_then_condition)
            query_params["balance_lt"] = less_then_condition

        db_count = (
            await dbsession.execute(
                select(
                    func.count(AccountModel.id).over().label("TotalFilteredAccounts")
                ).where(*db_filters)
            )
        ).scalar() or 0

        url = fastapi_app.url_path_for("get_accounts")
        response = await client.get(url, params=query_params)

        if db_count == 0:
            assert response.status_code == 404
        else:
            response_count = response.json()["metadata"]["total"]

            assert response.status_code == 200
            assert response_count == db_count
