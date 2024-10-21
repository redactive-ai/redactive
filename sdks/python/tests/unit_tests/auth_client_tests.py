from typing import Any
from urllib.parse import urlencode

import pytest

from redactive.auth_client import (
    AuthClient,
    BeginConnectionResponse,
    ExchangeTokenResponse,
)


def build_uri_query(data: dict[str, Any]) -> str:
    """Take dict and convert to query string and ignore None value"""
    return urlencode([(k, v) for k, v in data.items() if v is not None], doseq=True)


@pytest.fixture
def mock_client():
    return AuthClient(api_key="test_api_key", base_url="https://mock.api")


@pytest.mark.asyncio
async def test_begin_connection(mock_client, httpx_mock):
    provider = "provider"
    redirect_uri = "https://redirect.uri"
    state = "state123"
    expected_url = f"https://mock.api/api/auth/connect/provider/url?redirect_uri={redirect_uri}"
    httpx_mock.add_response(
        method="POST",
        url=f"https://mock.api/api/auth/connect/{provider}/url?{build_uri_query({"redirect_uri": redirect_uri, "state": state})}",
        json={"url": expected_url},
    )
    response = await mock_client.begin_connection("provider", redirect_uri, state="state123")
    assert response == BeginConnectionResponse(url=expected_url)


@pytest.mark.asyncio
async def test_exchange_tokens(mock_client, httpx_mock):
    code = "mock_code"
    refresh_token = "mock_refresh_token"
    httpx_mock.add_response(
        json={
            "idToken": "test-id-token",
            "refreshToken": "test-refresh-token",
            "expiresIn": 3600,
        }
    )
    exchange_response = await mock_client.exchange_tokens(code, refresh_token)
    assert isinstance(exchange_response, ExchangeTokenResponse)
