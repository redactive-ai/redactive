import base64
import json
from unittest import mock

import pytest

from redactive.auth_client import AuthClient
from redactive.grpc.v2 import RelevantChunk
from redactive.multi_user_client import MultiUserClient, UserData
from redactive.search_client import SearchClient


def mock_read_user_data(user_id) -> UserData | None:
    if user_id == "user123":
        return UserData(refresh_token="refreshToken123", id_token="idToken123")
    return None


@pytest.fixture
def mock_auth_client() -> mock.AsyncMock:
    return mock.AsyncMock(spec=AuthClient)


@pytest.fixture
def mock_search_client() -> mock.AsyncMock:
    return mock.AsyncMock(spec=SearchClient)


@pytest.fixture
def multi_user_client() -> MultiUserClient:
    return MultiUserClient(
        api_key="test_api_key",
        callback_uri="http://callback.uri",
        read_user_data=mock.AsyncMock(),
        write_user_data=mock.AsyncMock(),
        auth_base_url="http://auth.base.url",
        grpc_host="grpc.host",
        grpc_port=443,
    )


def test_multi_user_client_initialization() -> None:
    api_key = "test_api_key"
    callback_uri = "http://callback.uri"
    read_user_data = mock.Mock()
    write_user_data = mock.Mock()
    auth_base_url = "http://auth.base.url"
    grpc_host = "grpc.host"
    grpc_port = 443

    multi_user_client = MultiUserClient(
        api_key=api_key,
        callback_uri=callback_uri,
        read_user_data=read_user_data,
        write_user_data=write_user_data,
        auth_base_url=auth_base_url,
        grpc_host=grpc_host,
        grpc_port=grpc_port,
    )

    assert isinstance(multi_user_client.auth_client, AuthClient)
    assert isinstance(multi_user_client.search_client, SearchClient)
    assert multi_user_client.callback_uri == callback_uri
    assert multi_user_client.read_user_data == read_user_data
    assert multi_user_client.write_user_data == write_user_data
    assert multi_user_client.search_client.host == grpc_host
    assert multi_user_client.search_client.port == grpc_port


def test_multi_user_client_initialization_with_no_options() -> None:
    api_key = "test_api_key"
    callback_uri = "http://callback.uri"
    read_user_data = mock.Mock()
    write_user_data = mock.Mock()

    multi_user_client = MultiUserClient(
        api_key=api_key, callback_uri=callback_uri, read_user_data=read_user_data, write_user_data=write_user_data
    )

    assert isinstance(multi_user_client.auth_client, AuthClient)
    assert isinstance(multi_user_client.search_client, SearchClient)
    assert multi_user_client.callback_uri == callback_uri
    assert multi_user_client.read_user_data == read_user_data
    assert multi_user_client.write_user_data == write_user_data


@pytest.mark.asyncio
async def test_search_chunks(multi_user_client: MultiUserClient, mock_search_client: mock.AsyncMock) -> None:
    user_id = "user123"
    query = "example query"
    count = 5
    filters = {"key": "value"}
    relevant_chunks = [mock.Mock(spec=RelevantChunk) for _ in range(count)]

    multi_user_client.search_client = mock_search_client
    multi_user_client.search_client.search_chunks.return_value = relevant_chunks
    multi_user_client.read_user_data.side_effect = mock_read_user_data

    result = await multi_user_client.search_chunks(user_id, query, count, filters=filters)

    assert result == relevant_chunks
    multi_user_client.search_client.search_chunks.assert_called_with("idToken123", query, count, filters=filters)


@pytest.mark.asyncio
async def test_get_document_by_url(multi_user_client: MultiUserClient, mock_search_client: mock.AsyncMock) -> None:
    user_id = "user123"
    url = "http://example.com"
    chunks = [mock.Mock() for _ in range(3)]

    multi_user_client.search_client = mock_search_client
    multi_user_client.search_client.get_document.return_value = chunks
    multi_user_client.read_user_data.side_effect = mock_read_user_data

    result = await multi_user_client.get_document(user_id, url)

    assert result == chunks
    multi_user_client.search_client.get_document.assert_called_with("idToken123", url)


async def test_get_begin_connection_url(multi_user_client: MultiUserClient, mock_auth_client: mock.AsyncMock) -> None:
    user_id = "user123"
    provider = "google"
    state = "state123"
    url = "http://auth.url"

    with mock.patch("uuid.uuid4", return_value=state):
        mock_auth_client.begin_connection.return_value = mock.AsyncMock(url=url)
        multi_user_client.auth_client = mock_auth_client
        multi_user_client.read_user_data.return_value = UserData(sign_in_state=None)
        expected_user_data = UserData(sign_in_state=state)

        result = await multi_user_client.get_begin_connection_url(user_id, provider)

        assert result == url
        mock_auth_client.begin_connection.assert_called_with(provider, multi_user_client.callback_uri, state=state)
        multi_user_client.write_user_data.assert_called_with(user_id, expected_user_data)


@pytest.mark.asyncio
async def test_refresh_user_data(multi_user_client: MultiUserClient, mock_auth_client: mock.AsyncMock) -> None:
    user_id = "user123"
    refresh_token = "refreshToken123"
    id_token = "idToken123"
    expires_in = 3600
    connections = ["conn1", "conn2"]

    mock_auth_client.exchange_tokens.return_value = mock.AsyncMock(
        idToken=id_token, refreshToken=refresh_token, expiresIn=expires_in
    )
    mock_auth_client.list_connections.return_value = mock.AsyncMock(connections=connections)

    multi_user_client.auth_client = mock_auth_client
    multi_user_client.read_user_data.return_value = UserData(sign_in_state="state123")
    _ = await multi_user_client.handle_connection_callback(user_id, sign_in_code="signInCode123", state="state123")

    # extract what is the user data written after refresh token
    args, _ = multi_user_client.write_user_data.call_args
    written_user_data = args[1]

    expected_user_data = UserData(
        id_token=id_token,
        id_token_expiry=mock.ANY,
        refresh_token=refresh_token,
        connections=connections,
    )
    assert written_user_data == expected_user_data


@pytest.mark.asyncio
async def test_get_users_redactive_email_with_existing_token(multi_user_client: MultiUserClient) -> None:
    user_id = "user123"
    email = "user@example.com"

    # Create a valid JWT token with a base64-encoded payload and header
    payload = json.dumps({"email": email}).encode()
    header = json.dumps({"alg": "HS256", "typ": "JWT"}).encode()
    encoded_payload = base64.urlsafe_b64encode(payload).decode().rstrip("=")
    encoded_header = base64.urlsafe_b64encode(header).decode().rstrip("=")
    encoded_signature = base64.urlsafe_b64encode(b"signature").decode().rstrip("=")
    id_token = f"{encoded_header}.{encoded_payload}.{encoded_signature}"

    # Get user email when idToken found in UserData
    user_data_mock = mock.Mock(spec=UserData)
    user_data_mock.id_token = id_token
    multi_user_client.read_user_data.return_value = user_data_mock

    result = await multi_user_client.get_users_redactive_email(user_id)
    assert result == email


@pytest.mark.asyncio
async def test_get_users_redactive_email_with_no_token(multi_user_client: MultiUserClient) -> None:
    user_id = "user123"

    # Get user email when no idToken found in UserData
    user_data_mock = mock.Mock(spec=UserData)
    user_data_mock.id_token = None
    multi_user_client.read_user_data.return_value = user_data_mock

    result = await multi_user_client.get_users_redactive_email(user_id)
    assert result is None
