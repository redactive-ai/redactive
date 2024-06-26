# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: chunks.proto, search.proto
# plugin: python-betterproto
# This file has been @generated

from dataclasses import dataclass
from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Dict,
    List,
    Optional,
)

import betterproto
import betterproto.lib.google.protobuf as betterproto_lib_google_protobuf
import grpclib
from betterproto.grpc.grpclib_server import ServiceBase

if TYPE_CHECKING:
    import grpclib.server
    from betterproto.grpc.grpclib_client import MetadataLike
    from grpclib.metadata import Deadline


@dataclass(eq=False, repr=False)
class ChunkMetadata(betterproto.Message):
    created_at: Optional[datetime] = betterproto.message_field(1, optional=True, group="_created_at")
    """Chunk content's creation timestamp"""

    modified_at: Optional[datetime] = betterproto.message_field(2, optional=True, group="_modified_at")
    """Chunk content's last modified timestamp"""

    link: Optional[str] = betterproto.string_field(3, optional=True, group="_link")


@dataclass(eq=False, repr=False)
class SourceReference(betterproto.Message):
    system: str = betterproto.string_field(1)
    """Source system of the document e.g. confluence, slack, google-drive"""

    system_version: str = betterproto.string_field(2)
    """Version of the source system e.g. 1.0.0"""

    connection_id: str = betterproto.string_field(3)
    """
    Connection id to the source system e.g. confluence space id, slack channel
    id, google-drive drive id
    """

    document_id: str = betterproto.string_field(4)
    """
    Document id in the source system e.g. confluence page id, slack message id,
    google-drive document id
    """

    document_version: str = betterproto.string_field(5)
    """
    Document version in the source system e.g. confluence page version, slack
    message version, google-drive document version
    """

    document_path: Optional[str] = betterproto.string_field(6, optional=True, group="_document_path")
    """
    Document path in the source system e.g. "My Drive/document.txt", "slack-
    channel-name"
    """


@dataclass(eq=False, repr=False)
class ChunkReference(betterproto.Message):
    chunking_version: str = betterproto.string_field(1)
    """Chunking version e.g. 1.0.0"""

    chunk_id: str = betterproto.string_field(2)
    """chunk id is unique within the document, but not globally unique."""

    chunk_hash: str = betterproto.string_field(3)
    """SHA256 hash of the chunk body"""


@dataclass(eq=False, repr=False)
class RelevantChunk(betterproto.Message):
    """A chunk is a part of a document"""

    source: "SourceReference" = betterproto.message_field(1)
    """Source reference of the document"""

    chunk: "ChunkReference" = betterproto.message_field(2)
    """Chunk reference of the chunk"""

    relevance: "RelevantChunkRelevance" = betterproto.message_field(3)
    """Relevance of the chunk"""

    chunk_body: str = betterproto.string_field(4)
    """Chunk body"""

    document_metadata: "ChunkMetadata" = betterproto.message_field(5)
    """Document metadata"""


@dataclass(eq=False, repr=False)
class RelevantChunkRelevance(betterproto.Message):
    similarity_score: float = betterproto.float_field(1)
    """Similarity score of the chunk"""


@dataclass(eq=False, repr=False)
class Query(betterproto.Message):
    semantic_query: str = betterproto.string_field(1)
    """Semantic query to execute"""


@dataclass(eq=False, repr=False)
class TimeSpan(betterproto.Message):
    after: Optional[datetime] = betterproto.message_field(1, optional=True, group="_after")
    before: Optional[datetime] = betterproto.message_field(2, optional=True, group="_before")


@dataclass(eq=False, repr=False)
class Filters(betterproto.Message):
    scope: List[str] = betterproto.string_field(1)
    """
    Scope e.g. "confluence", "slack://channel-name", "google-
    drive://CompanyDrive/document.docx"
    """

    created: Optional["TimeSpan"] = betterproto.message_field(2, optional=True, group="_created")
    """Timespan of response chunk's creation"""

    modified: Optional["TimeSpan"] = betterproto.message_field(3, optional=True, group="_modified")
    """Timespan of response chunk's last modification"""

    user_emails: List[str] = betterproto.string_field(4)
    """List of user emails associated with response chunk"""


@dataclass(eq=False, repr=False)
class QueryRequest(betterproto.Message):
    count: Optional[int] = betterproto.uint32_field(1, optional=True, group="_count")
    """How many results to try to return (maximum number of results)"""

    query: "Query" = betterproto.message_field(2)
    """The query to execute"""

    filters: Optional["Filters"] = betterproto.message_field(3, optional=True, group="_filters")
    """Filters to apply to query"""


@dataclass(eq=False, repr=False)
class QueryResponse(betterproto.Message):
    success: bool = betterproto.bool_field(1)
    """Query was successful"""

    error: Optional["betterproto_lib_google_protobuf.Struct"] = betterproto.message_field(
        2, optional=True, group="_error"
    )
    """Error message if query failed"""

    relevant_chunks: List["RelevantChunk"] = betterproto.message_field(3)
    """List of relevant chunks"""


class SearchStub(betterproto.ServiceStub):
    async def query_chunks(
        self,
        query_request: "QueryRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> "QueryResponse":
        return await self._unary_unary(
            "/redactive.grpc.v1.Search/QueryChunks",
            query_request,
            QueryResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )


class SearchBase(ServiceBase):
    async def query_chunks(self, query_request: "QueryRequest") -> "QueryResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_query_chunks(self, stream: "grpclib.server.Stream[QueryRequest, QueryResponse]") -> None:
        request = await stream.recv_message()
        response = await self.query_chunks(request)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/redactive.grpc.v1.Search/QueryChunks": grpclib.const.Handler(
                self.__rpc_query_chunks,
                grpclib.const.Cardinality.UNARY_UNARY,
                QueryRequest,
                QueryResponse,
            ),
        }
