import { Metadata, ServiceError } from "@grpc/grpc-js";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { Chunk, ChunkReference, RelevantChunk, RelevantChunk_Relevance, SourceReference } from "./grpc/chunks";
import {
  Filters,
  GetDocumentRequest,
  GetDocumentResponse,
  SearchChunksRequest,
  SearchChunksResponse,
  SearchClient as SearchServiceClient
} from "./grpc/search";
import { SearchClient } from "./searchClient";

describe("Service client", () => {
  beforeEach(() => {});

  afterEach(() => {
    vi.clearAllMocks();
  });

  it("should get chunks by document reference", async () => {
    const accessToken = "test-accessToken";
    const ref = "test-documentName";
    const filters: Partial<Filters> = {
      scope: ["dataprovider"],
      created: { before: new Date() },
      modified: { after: new Date() },
      includeContentInTrash: true
    };
    const expectedResponse: Chunk[] = Array.from({ length: 5 }, (_, i) => ({
      source: {
        system: `system-${i}`,
        systemVersion: `systemVersion-${i}`,
        documentId: `documentId-${i}`,
        documentVersion: `documentVersion-${i}`,
        connectionId: `connectionId-${i}`,
        documentName: `documentName-${i}`,
        documentPath: `documentPath-${i}`
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
      getDocument: (
        _request: GetDocumentRequest,
        _metadata: Metadata,
        callback: (error: ServiceError | null, response: GetDocumentResponse) => void
      ) => callback(null, { success: true, chunks: expectedResponse } as GetDocumentResponse)
    } as unknown as SearchServiceClient);

    const client = new SearchClient();

    const response = await client.getDocument({ accessToken, ref, filters });

    expect(response).toStrictEqual(expectedResponse);
  });

  it("should search chunks semantically", async () => {
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
        documentName: `documentName-${i}`,
        documentPath: `documentPath-${i}`
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
      searchChunks: (
        _request: SearchChunksRequest,
        _metadata: Metadata,
        callback: (error: ServiceError | null, response: SearchChunksResponse) => void
      ) => callback(null, SearchChunksResponse.fromJSON({ relevantChunks: expectedResponse }))
    } as unknown as SearchServiceClient);

    // Create an instance of SearchClient
    const client = new SearchClient();

    // Call the queryChunks method and capture the response
    const response = await client.searchChunksBySemantics({ accessToken, query, count, filters });

    // Assert that the response matches the expected response
    expect(response).toStrictEqual(expectedResponse);
  });

  it("should search chunks by keyword", async () => {
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
        documentName: `documentName-${i}`,
        documentPath: `documentPath-${i}`
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
      searchChunks: (
        _request: SearchChunksRequest,
        _metadata: Metadata,
        callback: (error: ServiceError | null, response: SearchChunksResponse) => void
      ) => callback(null, SearchChunksResponse.fromJSON({ relevantChunks: expectedResponse }))
    } as unknown as SearchServiceClient);

    // Create an instance of SearchClient
    const client = new SearchClient();

    // Call the queryChunks method and capture the response
    const response = await client.searchChunksByKeyword({ accessToken, query, count, filters });

    // Assert that the response matches the expected response
    expect(response).toStrictEqual(expectedResponse);
  });
});
