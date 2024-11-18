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
    from redactive.grpc.v2 import Query, SearchChunksRequest

    access_token = "test-access_token"
    query = "Tell me about somethings"
    count = 1
    mock_channel_context.return_value.__aenter__.side_effect = mock.AsyncMock()

    with mock.patch("redactive.grpc.v2.SearchStub.search_chunks", side_effect=mock.AsyncMock()) as mock_query_chunks:
        client = SearchClient()
        await client.search_chunks(access_token, query, count)
        mock_query_chunks.assert_called_once_with(
            SearchChunksRequest(
                count=count,
                query=Query(query),
            )
        )


@mock.patch("grpclib.client.Channel")
@pytest.mark.asyncio
async def test_query_chunks_with_filter(mock_channel_context):
    from redactive.grpc.v2 import Filters, Query, SearchChunksRequest

    access_token = "test-access_token"
    query = "Tell me about somethings"
    count = 1
    filters = {"scope": "mock.scope"}
    mock_channel_context.return_value.__aenter__.side_effect = mock.AsyncMock()

    with mock.patch("redactive.grpc.v2.SearchStub.search_chunks", side_effect=mock.AsyncMock()) as mock_query_chunks:
        client = SearchClient()
        await client.search_chunks(access_token, query, count, filters)
        mock_query_chunks.assert_called_once_with(
            SearchChunksRequest(count=count, query=Query(query), filters=Filters(**filters))
        )


@mock.patch("grpclib.client.Channel")
@pytest.mark.asyncio
async def test_get_chunks_by_url(mock_channel_context):
    from redactive.grpc.v2 import GetDocumentRequest

    access_token = "test-access_token"
    url = "https://example.com"
    mock_channel_context.return_value.__aenter__.side_effect = mock.AsyncMock()

    with mock.patch(
        "redactive.grpc.v2.SearchStub.get_document", side_effect=mock.AsyncMock()
    ) as mock_get_chunks_by_url:
        client = SearchClient()
        await client.get_document(access_token, url)
        mock_get_chunks_by_url.assert_called_once_with(GetDocumentRequest(ref=url))
