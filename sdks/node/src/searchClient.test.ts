import { Metadata, ServiceError } from "@grpc/grpc-js";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { Chunk, ChunkReference, RelevantChunk, RelevantChunk_Relevance, SourceReference } from "./grpc/chunks";
import {
  Filters,
  GetChunksByUrlRequest,
  GetChunksByUrlResponse,
  QueryRequest,
  QueryResponse,
  SearchClient as SearchServiceClient
} from "./grpc/search";
import { SearchClient } from "./searchClient";

describe("Service client", () => {
  beforeEach(() => {});

  afterEach(() => {
    vi.clearAllMocks();
  });

  it("should query chunks", async () => {
    const accessToken = "test-accessToken";
    const query = "test-query";
    const count = 1;
    const filters: Partial<Filters> = {
      scope: ["dataprovider"],
      created: { before: new Date() },
      modified: { after: new Date() },
      includeContentInTrash: true
    };
    const expectedResponse: RelevantChunk[] = Array.from({ length: count }, (_, i) => ({
      source: {
        system: `system-${i}`,
        systemVersion: `systemVersion-${i}`,
        documentId: `documentId-${i}`,
        documentVersion: `documentVersion-${i}`,
        connectionId: `connectionId-${i}`,
        documentPath: undefined
      } as SourceReference,
      chunk: {
        chunkHash: `chunkHash-${i}`,
        chunkId: `chunkId-${i}`,
        chunkingVersion: `chunkingVersion-${i}`
      } as ChunkReference,
      chunkBody: `chunkBody-${i}`,
      documentMetadata: {
        createdAt: undefined,
        link: undefined,
        modifiedAt: undefined
      },
      relevance: {
        similarityScore: 1.0
      } as RelevantChunk_Relevance
    }));

    // Mock the _getClient method of SearchClient to return a mock gRPC client
    vi.spyOn(SearchClient.prototype, "_getClient").mockReturnValue({
      queryChunks: (
        _request: QueryRequest,
        _metadata: Metadata,
        callback: (error: ServiceError | null, response: QueryResponse) => void
      ) => callback(null, QueryResponse.fromJSON({ relevantChunks: expectedResponse }))
    } as unknown as SearchServiceClient);

    // Create an instance of SearchClient
    const client = new SearchClient();

    // Call the queryChunks method and capture the response
    const response = await client.queryChunks({ accessToken, semanticQuery: query, count, filters });

    // Assert that the response matches the expected response
    expect(response).toStrictEqual(expectedResponse);
  });

  it("should get chunks by url", async () => {
    const accessToken = "test-accessToken";
    const url = "https://example.com";
    const expectedResponse: Chunk[] = Array.from({ length: 10 }, (_, i) => ({
      source: {
        system: `system-${i}`,
        systemVersion: `systemVersion-${i}`,
        documentId: `documentId-${i}`,
        documentVersion: `documentVersion-${i}`,
        connectionId: `connectionId-${i}`,
        documentPath: undefined
      } as SourceReference,
      chunk: {
        chunkHash: `chunkHash-${i}`,
        chunkId: `chunkId-${i}`,
        chunkingVersion: `chunkingVersion-${i}`
      } as ChunkReference,
      chunkBody: `chunkBody-${i}`,
      documentMetadata: {
        createdAt: undefined,
        link: undefined,
        modifiedAt: undefined
      }
    }));

    // Mock the _getClient method of SearchClient to return a mock gRPC client
    vi.spyOn(SearchClient.prototype, "_getClient").mockReturnValue({
      getChunksByUrl: (
        _request: GetChunksByUrlRequest,
        _metadata: Metadata,
        callback: (error: ServiceError | null, response: GetChunksByUrlResponse) => void
      ) => callback(null, GetChunksByUrlResponse.fromJSON({ chunks: expectedResponse }))
    } as unknown as SearchServiceClient);

    // Create an instance of SearchClient
    const client = new SearchClient();

    // Call the getChunksByUrl method and capture the response
    const response = await client.getChunksByUrl({ accessToken, url });

    // Assert that the response matches the expected response
    expect(response).toStrictEqual(expectedResponse);
  });
});
