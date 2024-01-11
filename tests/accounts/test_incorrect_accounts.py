import pytest
from fastapi import FastAPI
from httpx import AsyncClient


@pytest.mark.anyio
async def test_page_size_zero(
    client: AsyncClient,
    fastapi_app: FastAPI,
) -> None:
    url = fastapi_app.url_path_for("get_accounts")
    response = await client.get(
        url,
        params={
            "page_size": 0,
            "page": 1,
        },
    )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_page_zero(
    client: AsyncClient,
    fastapi_app: FastAPI,
) -> None:
    url = fastapi_app.url_path_for("get_accounts")
    response = await client.get(
        url,
        params={
            "page_size": 10,
            "page": 0,
        },
    )

    assert response.status_code == 422
