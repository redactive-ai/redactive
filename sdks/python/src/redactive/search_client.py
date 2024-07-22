from grpclib.client import Channel

from redactive.grpc.v1 import Filters, Query, QueryRequest, RelevantChunk, SearchStub


class SearchClient:
    def __init__(self, host: str = "grpc.redactive.ai", port: int = 443) -> None:
        """
        Initialize the connection settings for the service.

        :param host: The hostname or IP address of the service, defaults to "grpc.redactive.ai"
        :type host: str, optional
        :param port: The port number to connect to, defaults to 443
        :type port: int, optional
        """
        self.access_token = None
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
