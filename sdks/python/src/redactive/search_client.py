from typing import Any

from grpclib.client import Channel

from redactive._connection_mode import get_default_grpc_host_and_port as _get_default_grpc_host_and_port
from redactive.grpc.v2 import (
    Filters,
    GetDocumentRequest,
    GetDocumentResponse,
    Query,
    SearchChunksRequest,
    SearchChunksResponse,
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

    async def search_chunks(
        self,
        access_token: str,
        query: str,
        count: int = 10,
        filters: Filters | dict[str, Any] | None = None,
    ) -> SearchChunksResponse:
        """
        Query for relevant chunks based on a semantic query.

        :param access_token: The user's Redactive access token.
        :type access_token: str
        :param query: The query string used to find relevant chunks.
        :type query: str
        :param count: The number of relevant chunks to retrieve. Defaults to 10.
        :type count: int, optional
        :param filters: The filters for relevant chunks. See `Filters` type.
        :type filters: Filters | dict[str, Any], optional
        :return: A list of relevant chunks that match the query
        :rtype: list[RelevantChunk]
        """
        async with Channel(self.host, self.port, ssl=True) as channel:
            stub = SearchStub(channel, metadata=({"authorization": f"Bearer {access_token}"}))

            _filters: Filters | None = None
            if isinstance(filters, Filters):
                _filters = filters
            elif isinstance(filters, dict):
                _filters = Filters(**filters)

            request = SearchChunksRequest(count=count, query=Query(semantic_query=query), filters=_filters)
            return await stub.search_chunks(request)

    async def get_document(
        self,
        access_token: str,
        ref: str,
    ) -> GetDocumentResponse:
        """
        Query for chunks by document name.

        :param access_token: The user's Redactive access token.
        :type access_token: str
        :param ref: A reference to the document we are retrieving.
        :type ref: str
        :return: The complete list of chunks for the matching document.
        :rtype: list[Chunk]
        """
        async with Channel(self.host, self.port, ssl=True) as channel:
            stub = SearchStub(channel, metadata=({"authorization": f"Bearer {access_token}"}))

            request = GetDocumentRequest(ref=ref)
            return await stub.get_document(request)
