import pytest

from redactive.auth_client import (
    AuthClient,
    BeginConnectionResponse,
    ExchangeTokenResponse,
)


@pytest.fixture
def mock_client():
    return AuthClient(api_key="test_api_key", base_url="https://mock.api")


@pytest.mark.asyncio
async def test_begin_connection(mock_client, httpx_mock):
    redirect_uri = "https://redirect.uri"
    expected_url = f"https://mock.api/api/auth/connect/provider/url?redirect_uri={redirect_uri}"
    httpx_mock.add_response(json={"url": expected_url})
    response = await mock_client.begin_connection("provider", redirect_uri)
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
