from typing import Optional

import httpx
from pydantic import BaseModel


class ExchangeTokenResponse(BaseModel):
    idToken: str
    refreshToken: str
    expiresIn: int


class AuthClient:
    def __init__(self, api_key: str, base_url: str = "https://api.redactive.ai"):
        """
        Initialize the connection settings for the service.

        Parameters:
            api_key (str): The API key used for authentication.
            base_url (str, optional): The base URL for the HTTP client. Defaults to "https://api.redactive.ai".
        Attributes:
            _client (httpx.AsyncClient): The HTTP client configured with base URL and Bearer authentication.
        """
        self._client = httpx.AsyncClient(base_url=f"{base_url}", auth=BearerAuth(api_key))

    async def begin_connection(self, provider: str, redirect_uri: str) -> str:
        """
        Initiates a connection process with a specified provider.

        Parameters:
            provider (str): The name of the provider to connect with.
            redirect_uri (str): The URI to redirect to after initiating the connection. Defaults to an empty string.

        Returns:
            str: The URL to redirect the user to for beginning the connection.

        Raises:
            httpx.HTTPStatusError: If the HTTP request returns an unsuccessful status code.
            httpx.RequestError: If an error occurs while making the HTTP request.
        """
        response = await self._client.post(
            url=f"/api/auth/connect/{provider}/url", params={"redirect_uri": redirect_uri}
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise httpx.RequestError(response.text)

    async def exchange_tokens(
        self, code: Optional[str] = None, refresh_token: Optional[str] = None
    ) -> ExchangeTokenResponse:
        """
        Exchange an authorization code and refresh token for access tokens.

        Parameters:
            code (str): The authorization code received from the OAuth flow.
            refresh_token (str): The refresh token used for token refreshing.

        Returns:
            ExchangeTokenResponse: An object containing access token and other token information.

        Raises:
            httpx.HTTPStatusError: If the HTTP request returns an unsuccessful status code.
            httpx.RequestError: If an error occurs while making the HTTP request.
        """

        body = dict()
        if code:
            body["code"] = code
        if refresh_token:
            body["refresh_token"] = refresh_token

        response = await self._client.post(url="/api/auth/token", json=body)
        if response.status_code == 200:
            return ExchangeTokenResponse(**response.json())
        else:
            raise httpx.RequestError(response.text)


class BearerAuth(httpx.Auth):
    def __init__(self, token):
        self.token = token

    def auth_flow(self, request):
        request.headers["Authorization"] = f"Bearer {self.token}"
        yield request
