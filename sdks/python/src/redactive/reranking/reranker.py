from dataclasses import dataclass

from rerankers import Reranker

from redactive import search_client
from redactive.grpc.v1 import RelevantChunk


@dataclass
class RerankingConfig:
    max_fetch_results: int = 100
    """ Maximum number of results to fetch from Redactive's search """
    fetch_multiplier: int = 10
    """ Multiply the number of results required by this multiplier before fetching them.
        The reranker will rerank all these results, and then pick the top_k based on
        the total number of results requested.
    """
    reranking_algorithm: str = "cross-encoder"
    """
    Reranking algorithm from https://github.com/AnswerDotAI/rerankers/tree/main
    If you would like to try a different algorithm, add it to the pyproject.toml dependencies for
    reranking.
    """


class RerankingSearchClient(search_client.SearchClient):
    def __init__(self, host: str = "grpc.redactive.ai", port: int = 443) -> None:
        super().__init__(host, port)
        self.conf = RerankingConfig

    async def query_chunks(
        self,
        access_token: str,
        semantic_query: str,
        count: int = 3,
        query_filter: dict | None = None,
    ) -> list[RelevantChunk]:
        # Get many more results than the uesr is asking for, then
        # rerank them
        big_fetch_count = count * self.conf.fetch_multiplier
        if big_fetch_count > self.conf.max_fetch_results:
            big_fetch_count = self.conf.max_fetch_results

        fetched_chunks = await super().query_chunks(access_token, semantic_query, big_fetch_count, query_filter)
        ranker = Reranker(self.conf.reranking_algorithm)
        return self.rerank(semantic_query, fetched_chunks, ranker, count)

    def rerank(self, query_string: str, fetched_chunks: list[RelevantChunk], ranker, top_k):
        """
        Rerank the results using reranking library, return top_k, as per original request

        :param query_string: Original query string
        :type query_string: str
        :param fetched_chunks: Chunks fetched from original query
        :type fetched_chunks: list[RelevantChunk]
        """
        docs = [c.chunk_body for c in fetched_chunks]
        ranker_results = ranker.rank(query_string, docs)
        merged_results = []
        for res in ranker_results:
            original_chunk = fetched_chunks[res.doc_id]
            original_chunk.relevance.similarity_score = res.score
            merged_results.append(original_chunk)

        return merged_results[:top_k]
