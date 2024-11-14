import warnings
from typing import Any
from urllib.parse import urlparse

from grpclib.client import Channel

from redactive._connection_mode import get_default_grpc_host_and_port as _get_default_grpc_host_and_port
from redactive.grpc.v2 import (
    Chunk,
    DocumentNameQuery,
    Filters,
    GetChunksByUrlRequest,
    Query,
    QueryByDocumentNameRequest,
    QueryRequest,
    RelevantChunk,
    SearchStub,
)


class SearchClient:
    def __init__(self, host: str | None = None, port: int | None = None) -> None:
        """
        Redactive API search client.

        :param host: The hostname or IP address of the Redactive API service.
        :type host: str, optional
        :param port: The port number of the Redactive API service.
        :type port: int, optional
        """
        if host is not None and port is None:
            msg = "Port must also be specified if host is specified"
            raise ValueError(msg)
        if port is not None and host is None:
            msg = "Host must also be specified if port is specified"
            raise ValueError(msg)
        if host is None and port is None:
            host, port = _get_default_grpc_host_and_port()

        self.host = host
        self.port = port

    async def query_chunks(
        self,
        access_token: str,
        semantic_query: str,
        count: int = 10,
        query_filter: dict[str, Any] | None = None,
        filters: Filters | dict[str, Any] | None = None,
    ) -> list[RelevantChunk]:
        """
        Query for relevant chunks based on a semantic query.

        :param access_token: The user's Redactive access token.
        :type access_token: str
        :param semantic_query: The query string used to find relevant chunks.
        :type semantic_query: str
        :param count: The number of relevant chunks to retrieve. Defaults to 10.
        :type count: int, optional
        :param query_filter: deprecated, use `filters`.
        :type query_filter: dict[str, Any], optional
        :param filters: The filters for relevant chunks. See `Filters` type.
        :type filters: Filters | dict[str, Any], optional
        :return: A list of relevant chunks that match the query
        :rtype: list[RelevantChunk]
        """
        if query_filter is not None:
            warnings.warn("`query_filter` has been renamed `filters``", DeprecationWarning, stacklevel=2)

        async with Channel(self.host, self.port, ssl=True) as channel:
            stub = SearchStub(channel, metadata=({"authorization": f"Bearer {access_token}"}))

            _filters: Filters | None = None
            if isinstance(filters, Filters):
                _filters = filters
            elif isinstance(filters, dict):
                _filters = Filters(**filters)
            elif query_filter is not None:
                _filters = Filters(**query_filter)

            request = QueryRequest(count=count, query=Query(semantic_query=semantic_query), filters=_filters)
            response = await stub.query_chunks(request)
            return response.relevant_chunks

    async def query_chunks_by_document_name(
        self,
        access_token: str,
        document_name: str,
        filters: Filters | dict[str, Any] | None = None,
    ) -> list[Chunk]:
        """
        Query for chunks by document name.

        :param access_token: The user's Redactive access token.
        :type access_token: str
        :param document_name: The name of the document to retrieve chunks.
        :type document_name: str
        :param filters: The filters for querying documents. See `Filters` type.
        :type filters: Filters | dict[str, Any], optional
        :return: The complete list of chunks for the matching document.
        :rtype: list[Chunk]
        """
        async with Channel(self.host, self.port, ssl=True) as channel:
            stub = SearchStub(channel, metadata=({"authorization": f"Bearer {access_token}"}))

            _filters: Filters | None = None
            if isinstance(filters, Filters):
                _filters = filters
            elif isinstance(filters, dict):
                _filters = Filters(**filters)

            request = QueryByDocumentNameRequest(query=DocumentNameQuery(document_name=document_name), filters=_filters)
            response = await stub.query_chunks_by_document_name(request)
            return response.chunks

    async def get_chunks_by_url(
        self,
        access_token: str,
        url: str,
    ) -> list[Chunk]:
        """
        Get chunks from a document by its URL.

        :param access_token: The user access token
        :type access_token: str
        :param url: The URL to the document for retrieving chunks.
        :type url: str
        :return: The complete list of chunks for the document.
        :rtype: list[Chunk]
        """
        async with Channel(self.host, self.port, ssl=True) as channel:
            stub = SearchStub(channel, metadata=({"authorization": f"Bearer {access_token}"}))

            parsed_url = urlparse(url)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                msg = "Url is not valid"
                raise ValueError(msg)

            request = GetChunksByUrlRequest(url=url)
            response = await stub.get_chunks_by_url(request)
            return response.chunks
