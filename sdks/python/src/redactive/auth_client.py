import http

import httpx
from pydantic import BaseModel

from redactive._connection_mode import get_default_http_endpoint as _get_default_http_endpoint


class ExchangeTokenResponse(BaseModel):
    idToken: str  # noqa: N815
    refreshToken: str  # noqa: N815
    expiresIn: int  # noqa: N815


class BeginConnectionResponse(BaseModel):
    url: str


class AuthClient:
    def __init__(self, api_key: str, base_url: str | None = None):
        """
        Initialize the connection settings for the service.

        :param api_key: The API key used for authentication.
        :type api_key: str
        :param base_url: The base URL to use for Redactive.
        :type base_url: str, optional
        """
        if base_url is None:
            base_url = _get_default_http_endpoint()

        self._client = httpx.AsyncClient(base_url=f"{base_url}", auth=BearerAuth(api_key))

    async def begin_connection(
        self, provider: str, redirect_uri: str, endpoint: str | None = None, code_param_alias: str | None = None
    ) -> BeginConnectionResponse:
        """
        Initiates a connection process with a specified provider.

        :param provider: The name of the provider to connect with.
        :type provider: str
        :param redirect_uri: The URI to redirect to after initiating the connection. Defaults to an empty string.
        :type redirect_uri: str
        :param endpoint: The endpoint to use to access specific provider APIs. Only required if connecting to Zendesk. Defaults to None.
        :type endpoint: str, optional
        :param code_param_alias: The alias for the code parameter. This is the name of the query parameter that will need to be passed to the `/auth/token` endpoint as `code`. Defaults to None and will be `code` on the return.
        :type code_param_alias: str, optional
        :raises httpx.RequestError: If an error occurs while making the HTTP request.
        :return: The URL to redirect the user to for beginning the connection.
        :rtype: BeginConnectionResponse
        """
        params = {"redirect_uri": redirect_uri}
        if endpoint:
            params["endpoint"] = endpoint
        if code_param_alias:
            params["code_param_alias"] = code_param_alias
        response = await self._client.post(url=f"/api/auth/connect/{provider}/url", params=params)
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
