import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

import jwt

from redactive.auth_client import AuthClient, ListConnectionsResponse
from redactive.grpc.v1 import Chunk, RelevantChunk
from redactive.search_client import SearchClient


@dataclass
class UserData:
    refresh_token: str | None = None
    id_token: str | None = None
    id_token_expiry: datetime | None = None
    connections: list[str] = field(default_factory=list)
    sign_in_state: str | None = None


@dataclass
class MultiUserClientConfig:
    auth_base_url: str
    """The base auth URL to use for Redactive."""
    grpc_host: str
    """The host to use for the gRPC server for Search services."""
    grpc_port: int
    """The port to use for the gRPC server for Search services."""


class InvalidRedactiveSessionError(Exception):
    def __init__(self, user_id: str) -> None:
        super().__init__(f"No valid Redactive session for user '{user_id}'")


class MultiUserClient:
    def __init__(
        self,
        api_key: str,
        callback_uri: str,
        read_user_data: Callable[[str], Awaitable[UserData]],
        write_user_data: Callable[[str, UserData | None], Awaitable[None]],
        config: MultiUserClientConfig,
    ) -> None:
        """Redactive client handling multiple users authentication and access to the Redactive Search service.

        :param api_key: Redactive API key.
        :type api_key: str
        :param callback_uri: The URI to redirect to after initiating the connection. Defaults to an empty string.
        :type callback_uri: str
        :param read_user_data: Function to read user data from storage.
        :type read_user_data: Callable[[str], Awaitable[UserData]]
        :param write_user_data: Function to write user data to storage.
        :type write_user_data: Callable[[str, UserData | None], Awaitable[None]]
        :param config: configuration of the auth client and the search client
        :type config: MultiUserClientConfig
        """

        self.auth_client = AuthClient(api_key, base_url=config.auth_base_url)
        self.search_client = SearchClient(config.grpc_host, config.grpc_port)
        self.callback_uri = callback_uri
        self.read_user_data = read_user_data
        self.write_user_data = write_user_data

    async def get_begin_connection_url(self, user_id: str, provider: str) -> str:
        state = str(uuid.uuid4())
        response = await self.auth_client.begin_connection(provider, self.callback_uri, code_param_alias=state)
        user_data: UserData = await self.read_user_data(user_id)
        user_data.sign_in_state = state
        await self.write_user_data(user_id, user_data)
        return response.url

    async def _refresh_user_data(
        self, user_id: str, refresh_token: str | None = None, sign_in_code: str | None = None
    ) -> UserData:
        tokens = await self.auth_client.exchange_tokens(sign_in_code, refresh_token)
        connections: ListConnectionsResponse = await self.auth_client.list_connections(tokens.idToken)
        user_data: UserData = UserData(
            tokens.refreshToken,
            tokens.idToken,
            datetime.now(UTC) + timedelta(seconds=tokens.expiresIn - 10),
            connections.connections,
        )
        await self.write_user_data(user_id, user_data)
        return user_data

    async def get_users_redactive_email(self, user_id: str) -> str | None:
        user_data = await self.read_user_data(user_id)
        if not user_data or not user_data.id_token:
            return None
        token_body = jwt.decode(user_data.id_token, options={"verify_signature": False})
        return token_body.get("email")

    async def handle_connection_callback(self, user_id: str, sign_in_code: str, state: str) -> bool:
        user_data = await self.read_user_data(user_id)
        if not user_data or user_data.sign_in_state != state:
            return False
        await self._refresh_user_data(user_id, sign_in_code=sign_in_code)
        return True

    async def get_user_connections(self, user_id: str) -> list[str]:
        user_data = await self.read_user_data(user_id)
        if user_data and user_data.id_token_expiry and user_data.id_token_expiry > datetime.now(UTC):
            return user_data.connections or []
        if user_data and user_data.refresh_token:
            user_data = await self._refresh_user_data(user_id, refresh_token=user_data.refresh_token)
            return user_data.connections or []
        return []

    async def clear_user_data(self, user_id: str) -> None:
        await self.write_user_data(user_id, None)

    async def _get_id_token(self, user_id: str) -> str:
        user_data = await self.read_user_data(user_id)
        if not user_data or not user_data.refresh_token:
            raise InvalidRedactiveSessionError(user_id)
        if user_data.id_token_expiry and user_data.id_token_expiry < datetime.now(UTC):
            user_data = await self._refresh_user_data(user_id, refresh_token=user_data.refresh_token)
        if not user_data.id_token:
            raise InvalidRedactiveSessionError(user_id)
        return user_data.id_token

    async def query_chunks(
        self, user_id: str, semantic_query: str, count: int = 10, filters: dict | None = None
    ) -> list[RelevantChunk]:
        id_token = await self._get_id_token(user_id)
        return await self.search_client.query_chunks(id_token, semantic_query, count, filters)

    async def query_chunks_by_document_name(
        self, user_id: str, document_name: str, filters: dict | None = None
    ) -> list[Chunk]:
        id_token = await self._get_id_token(user_id)
        return await self.search_client.query_chunks_by_document_name(id_token, document_name, filters)

    async def get_chunks_by_url(self, user_id: str, url: str) -> list[Chunk]:
        id_token = await self._get_id_token(user_id)
        return await self.search_client.get_chunks_by_url(id_token, url)
