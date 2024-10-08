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

    document_name: Optional[str] = betterproto.string_field(7, optional=True, group="_document_name")
    """Document name in the source system e.g. "document.txt"""


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
class Chunk(betterproto.Message):
    """A chunk is a part of a document"""

    source: "SourceReference" = betterproto.message_field(1)
    """Source reference of the document"""

    chunk: "ChunkReference" = betterproto.message_field(2)
    """Chunk reference of the chunk"""

    chunk_body: str = betterproto.string_field(3)
    """Chunk body"""

    document_metadata: "ChunkMetadata" = betterproto.message_field(4)
    """Document metadata"""


@dataclass(eq=False, repr=False)
class Query(betterproto.Message):
    semantic_query: str = betterproto.string_field(1)
    """Semantic query to execute"""


@dataclass(eq=False, repr=False)
class DocumentNameQuery(betterproto.Message):
    document_name: str = betterproto.string_field(1)
    """Document name to search for"""


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

    include_content_in_trash: Optional[bool] = betterproto.bool_field(
        5, optional=True, group="_include_content_in_trash"
    )
    """Include content from documents in trash"""


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


@dataclass(eq=False, repr=False)
class GetChunksByUrlRequest(betterproto.Message):
    url: str = betterproto.string_field(1)
    """URL to document"""


@dataclass(eq=False, repr=False)
class GetChunksByUrlResponse(betterproto.Message):
    success: bool = betterproto.bool_field(1)
    """Fetch was successful"""

    error: Optional["betterproto_lib_google_protobuf.Struct"] = betterproto.message_field(
        2, optional=True, group="_error"
    )
    """Error message if fetch failed"""

    chunks: List["Chunk"] = betterproto.message_field(3)
    """List of chunks"""


@dataclass(eq=False, repr=False)
class QueryByDocumentNameRequest(betterproto.Message):
    query: "DocumentNameQuery" = betterproto.message_field(2)
    """The query to execute"""

    filters: Optional["Filters"] = betterproto.message_field(3, optional=True, group="_filters")
    """Filters to apply to query"""


@dataclass(eq=False, repr=False)
class QueryByDocumentNameResponse(betterproto.Message):
    success: bool = betterproto.bool_field(1)
    """Query was successful"""

    error: Optional["betterproto_lib_google_protobuf.Struct"] = betterproto.message_field(
        2, optional=True, group="_error"
    )
    """Error message if query failed"""

    chunks: List["Chunk"] = betterproto.message_field(3)
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

    async def query_chunks_by_document_name(
        self,
        query_by_document_name_request: "QueryByDocumentNameRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> "QueryByDocumentNameResponse":
        return await self._unary_unary(
            "/redactive.grpc.v1.Search/QueryChunksByDocumentName",
            query_by_document_name_request,
            QueryByDocumentNameResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def get_chunks_by_url(
        self,
        get_chunks_by_url_request: "GetChunksByUrlRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None,
    ) -> "GetChunksByUrlResponse":
        return await self._unary_unary(
            "/redactive.grpc.v1.Search/GetChunksByUrl",
            get_chunks_by_url_request,
            GetChunksByUrlResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )


class SearchBase(ServiceBase):
    async def query_chunks(self, query_request: "QueryRequest") -> "QueryResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def query_chunks_by_document_name(
        self, query_by_document_name_request: "QueryByDocumentNameRequest"
    ) -> "QueryByDocumentNameResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def get_chunks_by_url(self, get_chunks_by_url_request: "GetChunksByUrlRequest") -> "GetChunksByUrlResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_query_chunks(self, stream: "grpclib.server.Stream[QueryRequest, QueryResponse]") -> None:
        request = await stream.recv_message()
        response = await self.query_chunks(request)
        await stream.send_message(response)

    async def __rpc_query_chunks_by_document_name(
        self,
        stream: "grpclib.server.Stream[QueryByDocumentNameRequest, QueryByDocumentNameResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.query_chunks_by_document_name(request)
        await stream.send_message(response)

    async def __rpc_get_chunks_by_url(
        self,
        stream: "grpclib.server.Stream[GetChunksByUrlRequest, GetChunksByUrlResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.get_chunks_by_url(request)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/redactive.grpc.v1.Search/QueryChunks": grpclib.const.Handler(
                self.__rpc_query_chunks,
                grpclib.const.Cardinality.UNARY_UNARY,
                QueryRequest,
                QueryResponse,
            ),
            "/redactive.grpc.v1.Search/QueryChunksByDocumentName": grpclib.const.Handler(
                self.__rpc_query_chunks_by_document_name,
                grpclib.const.Cardinality.UNARY_UNARY,
                QueryByDocumentNameRequest,
                QueryByDocumentNameResponse,
            ),
            "/redactive.grpc.v1.Search/GetChunksByUrl": grpclib.const.Handler(
                self.__rpc_get_chunks_by_url,
                grpclib.const.Cardinality.UNARY_UNARY,
                GetChunksByUrlRequest,
                GetChunksByUrlResponse,
            ),
        }
