import http

import httpx
from pydantic import BaseModel

from redactive._connection_mode import get_default_http_endpoint as _get_default_http_endpoint


class ListConnectionsResponse(BaseModel):
    user_id: str
    connections: list[str]


class ExchangeTokenResponse(BaseModel):
    idToken: str  # noqa: N815
    refreshToken: str  # noqa: N815
    expiresIn: int  # noqa: N815


class BeginConnectionResponse(BaseModel):
    url: str


class AuthClient:
    def __init__(self, api_key: str, base_url: str | None = None):
        """
        Initialize the connection settings for the Redactive API.

        :param api_key: The API key used for authentication.
        :type api_key: str
        :param base_url: The base URL to the Redactive API.
        :type base_url: str, optional
        """
        if base_url is None:
            base_url = _get_default_http_endpoint()

        self._client = httpx.AsyncClient(base_url=f"{base_url}", auth=BearerAuth(api_key))

    async def begin_connection(
        self,
        provider: str,
        redirect_uri: str,
        endpoint: str | None = None,
        code_param_alias: str | None = None,
        state: str | None = None,
    ) -> BeginConnectionResponse:
        """
        Return a URL for authorizing Redactive to connect with provider on a user's behalf.

        :param provider: The name of the provider to connect with.
        :type provider: str
        :param redirect_uri: The URI to redirect to after initiating the connection.
        :type redirect_uri: str
        :param endpoint: The endpoint to use to access specific provider APIs. Only required if connecting to Zendesk.
        :type endpoint: str, optional
        :param code_param_alias: The alias for the code parameter. This is the name of the query parameter that will need to be passed to the `/auth/token` endpoint as `code`. Defaults to None and will be `code` on the return.
        :type code_param_alias: str, optional
        :param state: An optional parameter that is stored as app_callback_state for building callback url.
        :type state: str, optional
        :raises httpx.RequestError: If an error occurs while making the HTTP request.
        :return: The URL to redirect the user to for beginning the connection.
        :rtype: BeginConnectionResponse
        """
        params = {"redirect_uri": redirect_uri}
        if endpoint:
            params["endpoint"] = endpoint
        if code_param_alias:
            params["code_param_alias"] = code_param_alias
        if state:
            params["state"] = state
        response = await self._client.post(url=f"/api/auth/connect/{provider}/url", params=params)
        if response.status_code != http.HTTPStatus.OK:
            raise httpx.RequestError(response.text)

        return BeginConnectionResponse(**response.json())

    async def exchange_tokens(self, code: str | None = None, refresh_token: str | None = None) -> ExchangeTokenResponse:
        """
        Exchange an authorization code and refresh token for access tokens.

        :param code: The authorization code received from the OAuth flow.
        :type code: str, optional
        :param refresh_token: The refresh token used for token refreshing.
        :type refresh_token: str, optional
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

    async def list_connections(self, access_token: str) -> ListConnectionsResponse:
        """
        Retrieve the list of user's provider connections.

        :param access_token: The user's access token for authentication..
        :type access_token: str
        :raises httpx.RequestError: If an error occurs while making the HTTP request.
        :return: An object containing the user ID and current connections.
        :rtype: UserConnections
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await self._client.get("/api/auth/connections", headers=headers)

        if response.status_code != http.HTTPStatus.OK:
            raise httpx.RequestError(response.text)

        return ListConnectionsResponse(**response.json())


class BearerAuth(httpx.Auth):
    def __init__(self, token):
        self.token = token

    def auth_flow(self, request):
        request.headers["Authorization"] = f"Bearer {self.token}"
        yield request
