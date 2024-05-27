from unittest import mock

import pytest

from redactive.search_client import SearchClient


def test_init_client():
    host = "grpc.redactive.ai"

    client = SearchClient()
    assert client.host == host


@mock.patch("grpclib.client.Channel")
@pytest.mark.asyncio
async def test_query_chunks(mock_channel_context):
    from redactive.grpc.v1 import Query, QueryRequest

    access_token = "test-access_token"
    semantic_query = "Tell me about somethings"
    count = 1
    mock_channel_context.return_value.__aenter__.side_effect = mock.AsyncMock()

    with mock.patch("redactive.grpc.v1.SearchStub.query_chunks", side_effect=mock.AsyncMock()) as mock_query_chunks:
        client = SearchClient()
        client.authenticate(access_token)
        await client.query_chunks(semantic_query, count)
        mock_query_chunks.assert_called_once_with(
            QueryRequest(
                count=count,
                query=Query(semantic_query),
            )
        )