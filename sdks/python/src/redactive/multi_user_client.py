import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any

import jwt

from redactive.auth_client import AuthClient
from redactive.grpc.v2 import Filters, GetDocumentResponse, SearchChunksResponse
from redactive.search_client import SearchClient


@dataclass
class UserData:
    refresh_token: str | None = None
    id_token: str | None = None
    id_token_expiry: datetime | None = None
    connections: list[str] = field(default_factory=list)
    sign_in_state: str | None = None


class InvalidRedactiveSessionError(Exception):
    def __init__(self, user_id: str) -> None:
        super().__init__(f"No valid Redactive session for user '{user_id}'")


class MultiUserClient:
    def __init__(
        self,
        api_key: str,
        callback_uri: str,
        read_user_data: Callable[[Annotated[str, "user_id"]], Awaitable[UserData]],
        write_user_data: Callable[[Annotated[str, "user_id"], UserData | None], Awaitable[None]],
        *,
        auth_base_url: str | None = None,
        grpc_host: str | None = None,
        grpc_port: int | None = None,
    ) -> None:
        """
        Redactive client handling multiple users authentication and access to the Redactive Search service.

        :param api_key: Redactive API key.
        :type api_key: str
        :param callback_uri: The URI to redirect to after initiating the connection.
        :type callback_uri: str
        :param read_user_data: Function to read user data from storage.
        :type read_user_data: Callable[[Annotated[str, user_id]], Awaitable[UserData]]
        :param write_user_data: Function to write user data to storage.
        :type write_user_data: Callable[[[Annotated[str, user_id], UserData | None], Awaitable[None]]
        :param auth_base_url: Base URL for the authentication service. Optional.
        :type auth_base_url: str | None
        :param grpc_host: Host for the Redactive API service. Optional.
        :type grpc_host: str | None
        :param grpc_port: Port for the Redactive API service. Optional.
        :type grpc_port: int | None
        """

        self.auth_client = AuthClient(api_key, base_url=auth_base_url)
        self.search_client = SearchClient(host=grpc_host, port=grpc_port)
        self.callback_uri = callback_uri
        self.read_user_data = read_user_data
        self.write_user_data = write_user_data

    async def get_begin_connection_url(self, user_id: str, provider: str) -> str:
        """
        Return a URL for authorizing Redactive to connect with provider on a user's behalf.

        :param user_id: A user ID to associate connection URL with.
        :type user_id: str
        :param provider: The name of the provider to connect with.
        :type provider: str
        :return: The URL to redirect the user to for beginning the connection.
        :rtype: str
        """
        state = str(uuid.uuid4())
        response = await self.auth_client.begin_connection(provider, self.callback_uri, state=state)
        user_data = await self.read_user_data(user_id)
        user_data.sign_in_state = state
        await self.write_user_data(user_id, user_data)
        return response.url

    async def _refresh_user_data(
        self, user_id: str, refresh_token: str | None = None, sign_in_code: str | None = None
    ) -> UserData:
        tokens = await self.auth_client.exchange_tokens(sign_in_code, refresh_token)
        connections = await self.auth_client.list_connections(tokens.idToken)
        user_data = UserData(
            refresh_token=tokens.refreshToken,
            id_token=tokens.idToken,
            id_token_expiry=datetime.now(UTC) + timedelta(seconds=tokens.expiresIn - 10),
            connections=connections.connections,
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
        """
        The callback method for users completing the connection flow; to be called when user returns to app with
        connection-related URL query parameters.

        :param user_id: The ID of the user completing their connection flow.
        :type user_id: str
        :param sign_in_code: The connection sign-in code returned in the URL query params by completing the connection flow.
        :type sign_in_code: str
        :param state: The state value returned in the URL query params by completing the connection flow.`
        :type state: str
        :return: A boolean represent successful connection completion.
        :rtype: bool
        """
        user_data = await self.read_user_data(user_id)
        if not user_data or user_data.sign_in_state != state:
            return False
        await self._refresh_user_data(user_id, sign_in_code=sign_in_code)
        return True

    async def get_user_connections(self, user_id: str) -> list[str]:
        """
        Retrieve the list of user's provider connections.
        :param user_id: The ID of the user.
        :type user_id: str
        :return: A list of user's connected providers.
        """
        user_data = await self.read_user_data(user_id)
        if user_data and user_data.id_token_expiry and user_data.id_token_expiry > datetime.now(UTC):
            return user_data.connections
        if user_data and user_data.refresh_token:
            user_data = await self._refresh_user_data(user_id, refresh_token=user_data.refresh_token)
            return user_data.connections
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

    async def search_chunks(
        self, user_id: str, query: str, count: int = 10, filters: Filters | dict[str, Any] | None = None
    ) -> SearchChunksResponse:
        """
        Query for relevant chunks based on a semantic query.

        :param user_id: The ID of the user.
        :type user_id: str
        :param query: The query string used to find relevant chunks.
        :type query: str
        :param count: The number of relevant chunks to retrieve. Defaults to 10.
        :type count: int, optional
        :param filters: The filters for relevant chunks. See `Filters` type.
        :type filters: Filters | dict[str, Any], optional
        :return: A list of relevant chunks that match the query
        :rtype: list[RelevantChunk]
        """
        id_token = await self._get_id_token(user_id)
        return await self.search_client.search_chunks(id_token, query, count, filters=filters)

    async def get_document(self, user_id: str, ref: str) -> GetDocumentResponse:
        """
        Get chunks from a document by its URL.

        :param user_id: The ID of the user.
        :type user_id: str
        :param url: The URL to the document for retrieving chunks.
        :type url: str
        :return: The complete list of chunks for the document.
        :rtype: list[Chunk]
        """
        id_token = await self._get_id_token(user_id)
        return await self.search_client.get_document(id_token, ref)
