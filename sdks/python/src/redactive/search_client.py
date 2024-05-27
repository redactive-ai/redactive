from typing import List

from grpclib.client import Channel

from redactive.grpc.v1 import Query, QueryRequest, RelevantChunk, SearchStub


class SearchClient:
    def __init__(self, host: str = "grpc.redactive.ai", port: int = 443) -> None:
        """
        Initialize the connection settings for the service.

        Parameters:
            host (str, optional): The hostname or IP address of the service. Defaults to "grpc.redactive.ai".
            port (int, optional): The port number to connect to. Defaults to 443.
        """
        self.access_token = None
        self.host = host
        self.port = port

    async def query_chunks(self, access_token: str, semantic_query: str, count: int = 1) -> List[RelevantChunk]:
        """
        Query for relevant chunks based on a semantic query.

        Parameters:
            semantic_query (str): The query string used to find relevant chunks.
            count (int, optional): The number of relevant chunks to retrieve. Defaults to 1.

        Returns:
            List[RelevantChunk]: A list of relevant chunks that match the query.
        """
        async with Channel(self.host, self.port, ssl=True) as channel:
            stub = SearchStub(channel, metadata=(dict(authorization=f"Bearer {access_token}")))
            request = QueryRequest(count=count, query=Query(semantic_query=semantic_query))
            response = await stub.query_chunks(request)
            return response.relevant_chunks
