import { Client, credentials, Metadata } from "@grpc/grpc-js";

import { Chunk, RelevantChunk } from "./grpc/chunks";
import {
  DocumentNameQuery,
  Filters,
  GetChunksByUrlRequest,
  GetChunksByUrlResponse,
  Query,
  QueryByDocumentNameRequest,
  QueryByDocumentNameResponse,
  QueryRequest,
  QueryResponse,
  SearchClient as SearchServiceClient
} from "./grpc/search";

export interface QueryChunksSearchParams {
  accessToken: string;
  semanticQuery: string;
  count?: number;
  filters?: Partial<Filters>;
}

export interface QueryChunksByDocumentNameSearchParams {
  accessToken: string;
  documentName: string;
  filters?: Partial<Filters>;
}

export interface GetChunksByUrlSearchParams {
  accessToken: string;
  url: string;
}

export class SearchClient {
  host: string = "grpc.redactive.ai";
  port: number = 443;
  _cachedServiceClients: Map<string, Client>;

  /**
   * Redactive API search client.
   * @param host - The hostname or IP address of the Redactive API service.
   * @param port - The port number of the Redactive API service.
   */
  constructor(host?: string, port?: number) {
    this.host = host || this.host;
    this.port = port || this.port;
    this._cachedServiceClients = new Map();
  }

  _getClient(service: string) {
    const client = this._cachedServiceClients.get(service);
    if (client) {
      return client;
    } else if (service == SearchServiceClient.serviceName) {
      const secureChannel = credentials.createSsl();
      const credential = credentials.combineChannelCredentials(secureChannel);
      const address = `${this.host}:${this.port}`;
      return new SearchServiceClient(address, credential);
    }
  }

  /**
   * Query for relevant chunks based on a semantic query.
   * @param accessToken - The user's Redactive access token.
   * @param semanticQuery - The query string used to find relevant chunks.
   * @param count - The number of relevant chunks to retrieve. Defaults to 10.
   * @param filters - An object of filters for querying. Optional.
   * @returns list of relevant chunks.
   */
  async queryChunks({
    accessToken,
    semanticQuery,
    count = 10,
    filters
  }: QueryChunksSearchParams): Promise<RelevantChunk[]> {
    const requestMetadata = new Metadata();
    requestMetadata.set("Authorization", `Bearer ${accessToken}`);
    requestMetadata.set("User-Agent", "redactive-sdk-node");

    const client = this._getClient(SearchServiceClient.serviceName) as SearchServiceClient;
    const query: Query = { semanticQuery };
    const _filters: Filters = { scope: [], userEmails: [], ...filters };
    const queryRequest: QueryRequest = {
      query,
      count,
      filters: filters ? _filters : undefined
    };

    const response = await new Promise<QueryResponse>((resolve, reject) => {
      client.queryChunks(queryRequest, requestMetadata, (err, response) => {
        if (err) {
          reject(err);
          return;
        }

        return resolve(response);
      });
    });
    return response.relevantChunks;
  }

  /**
   * Query for chunks by document name.
   * @param accessToken - The user's Redactive access token.
   * @param documentName - The name of the document to retrieve chunks.
   * @param filters - The filters for querying documents. Optional.
   * @returns The complete list of chunks for the matching document.
   */
  async queryChunksByDocumentName({
    accessToken,
    documentName,
    filters
  }: QueryChunksByDocumentNameSearchParams): Promise<Chunk[]> {
    const requestMetadata = new Metadata();
    requestMetadata.set("Authorization", `Bearer ${accessToken}`);
    requestMetadata.set("User-Agent", "redactive-sdk-node");

    const client = this._getClient(SearchServiceClient.serviceName) as SearchServiceClient;
    const query: DocumentNameQuery = { documentName };
    const _filters: Filters = { scope: [], userEmails: [], ...filters };
    const queryRequest: QueryByDocumentNameRequest = {
      query,
      filters: filters ? _filters : undefined
    };

    const response = await new Promise<QueryByDocumentNameResponse>((resolve, reject) => {
      client.queryChunksByDocumentName(queryRequest, requestMetadata, (err, response) => {
        if (err) {
          reject(err);
          return;
        }

        return resolve(response);
      });
    });
    return response.chunks;
  }

  /**
   * Get chunks from a document by its URL.
   * @param accessToken - The user's Redactive access token.
   * @param url - The URL to the document for retrieving chunks.
   * @returns The complete list of chunks for the matching document.
   */
  async getChunksByUrl({ accessToken, url }: GetChunksByUrlSearchParams): Promise<Chunk[]> {
    const requestMetadata = new Metadata();
    requestMetadata.set("Authorization", `Bearer ${accessToken}`);
    requestMetadata.set("User-Agent", "redactive-sdk-node");

    const client = this._getClient(SearchServiceClient.serviceName) as SearchServiceClient;
    const queryRequest: GetChunksByUrlRequest = {
      url
    };

    const response = await new Promise<GetChunksByUrlResponse>((resolve, reject) => {
      client.getChunksByUrl(queryRequest, requestMetadata, (err, response) => {
        if (err) {
          reject(err);
          return;
        }

        return resolve(response);
      });
    });
    return response.chunks;
  }
}
