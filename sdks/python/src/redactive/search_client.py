from urllib.parse import urlparse

from grpclib.client import Channel

from redactive._connection_mode import get_default_grpc_host_and_port as _get_default_grpc_host_and_port
from redactive.grpc.v1 import Chunk, Filters, GetChunksByUrlRequest, Query, QueryRequest, RelevantChunk, SearchStub


class SearchClient:
    def __init__(self, host: str | None = None, port: int | None = None) -> None:
        """
        Initialize the connection settings for the service.

        :param host: The hostname or IP address of the service
        :type host: str, optional
        :param port: The port number to connect to
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
        count: int = 1,
        query_filter: dict | None = None,
    ) -> list[RelevantChunk]:
        """
        Query for relevant chunks based on a semantic query.

        :param access_token: The user access token for querying
        :type access_token: str
        :param semantic_query: The query string used to find relevant chunks
        :type semantic_query: str
        :param count: The number of relevant chunks to retrieve, defaults to 1
        :type count: int, optional
        :param query_filter: The filters for filtering chunks, defaults to None
        :type query_filter: dict | None, optional
        :return: A list of relevant chunks that match the query
        :rtype: list[RelevantChunk]
        """
        async with Channel(self.host, self.port, ssl=True) as channel:
            stub = SearchStub(channel, metadata=({"authorization": f"Bearer {access_token}"}))

            filters = None
            if query_filter is not None:
                filters = Filters(**query_filter)

            request = QueryRequest(count=count, query=Query(semantic_query=semantic_query), filters=filters)
            response = await stub.query_chunks(request)
            return response.relevant_chunks

    async def get_chunks_by_url(
        self,
        access_token: str,
        url: str,
    ) -> list[Chunk]:
        """
        Get chunks from a document by its URL.

        :param access_token: The user access token
        :type access_token: str
        :param url: URL to source document to retrieve chunks
        :type url: str
        :return: A list of chunks from URL source document
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
