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

    async def begin_connection(
        self, provider: str, redirect_uri: str, endpoint: str | None = None, state: str | None = None
    ) -> str:
        """
        Initiates a connection process with a specified provider.

        Parameters:
            provider (str): The name of the provider to connect with.
            redirect_uri (str): The URI to redirect to after initiating the connection. Defaults to an empty string.
            endpoint (str | None): The data provider endpoint URL.
            state (str | None): The custom state parameter passed from the application.

        Returns:
            str: The URL to redirect the user to for beginning the connection.

        Raises:
            httpx.HTTPStatusError: If the HTTP request returns an unsuccessful status code.
            httpx.RequestError: If an error occurs while making the HTTP request.
        """

        params = {"redirect_uri": redirect_uri, "endpoint": endpoint, "state": state}
        async with self._client as client:
            response = await client.post(
                url=f"/api/auth/connect/{provider}/url",
                params={k: v for k, v in params.items() if v},
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise httpx.RequestError(response.text)

    async def exchange_tokens(self, code: str, refresh_token: str) -> ExchangeTokenResponse:
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
        async with self._client as client:
            response = await client.post(url="/api/auth/token", json={"code": code, "refresh_token": refresh_token})
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
