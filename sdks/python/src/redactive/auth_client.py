import http

import httpx
from pydantic import BaseModel


class ExchangeTokenResponse(BaseModel):
    idToken: str  # noqa: N815
    refreshToken: str  # noqa: N815
    expiresIn: int  # noqa: N815


class BeginConnectionResponse(BaseModel):
    url: str


class AuthClient:
    def __init__(self, api_key: str, base_url: str = "https://api.redactive.ai"):
        """
        Initialize the connection settings for the service.

        :param api_key: The API key used for authentication.
        :type api_key: str
        :param base_url: The base URL for the HTTP client, defaults to "https://api.redactive.ai"
        :type base_url: str, optional
        """

        self._client = httpx.AsyncClient(base_url=f"{base_url}", auth=BearerAuth(api_key))

    async def begin_connection(self, provider: str, redirect_uri: str) -> BeginConnectionResponse:
        """
        Initiates a connection process with a specified provider.

        :param provider: The name of the provider to connect with.
        :type provider: str
        :param redirect_uri: The URI to redirect to after initiating the connection. Defaults to an empty string.
        :type redirect_uri: str
        :raises httpx.RequestError: If an error occurs while making the HTTP request.
        :return: The URL to redirect the user to for beginning the connection.
        :rtype: BeginConnectionResponse
        """
        response = await self._client.post(
            url=f"/api/auth/connect/{provider}/url",
            params={"redirect_uri": redirect_uri},
        )
        if response.status_code != http.HTTPStatus.OK:
            raise httpx.RequestError(response.text)

        return BeginConnectionResponse(**response.json())

    async def exchange_tokens(self, code: str | None = None, refresh_token: str | None = None) -> ExchangeTokenResponse:
        """
        Exchange an authorization code and refresh token for access tokens.

        :param code: The authorization code received from the OAuth flow, defaults to None
        :type code: str | None, optional
        :param refresh_token: The refresh token used for token refreshing, defaults to None
        :type refresh_token: str | None, optional
        :raises httpx.RequestError: If an error occurs while making the HTTP request.
        :return: An object containing access token and other token information.
        :rtype: ExchangeTokenResponse
        """

        body = {}
        if code:
            body["code"] = code
        if refresh_token:
            body["refresh_token"] = refresh_token

        response = await self._client.post(url="/api/auth/token", json=body)
        if response.status_code != http.HTTPStatus.OK:
            raise httpx.RequestError(response.text)

        return ExchangeTokenResponse(**response.json())


class BearerAuth(httpx.Auth):
    def __init__(self, token):
        self.token = token

    def auth_flow(self, request):
        request.headers["Authorization"] = f"Bearer {self.token}"
        yield request
