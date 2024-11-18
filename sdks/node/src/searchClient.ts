import { Client, credentials, Metadata } from "@grpc/grpc-js";

import { Chunk, RelevantChunk } from "./grpc/chunks";
import {
  Filters,
  GetDocumentRequest,
  GetDocumentResponse,
  Query,
  SearchChunksRequest,
  SearchChunksResponse,
  SearchClient as SearchServiceClient
} from "./grpc/search";

export interface SearchChunksParams {
  accessToken: string;
  query: string;
  count?: number;
  filters?: Partial<Filters>;
}

export interface GetDocumentParams {
  accessToken: string;
  ref: string;
  filters?: Partial<Filters>;
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
   * @param query - The query string used to find relevant chunks.
   * @param count - The number of relevant chunks to retrieve. Defaults to 10.
   * @param filters - An object of filters for querying. Optional.
   * @returns list of relevant chunks.
   */
  async searchChunks({
    accessToken,
    query,
    count = 10,
    filters
  }: SearchChunksParams): Promise<RelevantChunk[]> {
    const requestMetadata = new Metadata();
    requestMetadata.set("Authorization", `Bearer ${accessToken}`);
    requestMetadata.set("User-Agent", "redactive-sdk-node");

    const client = this._getClient(SearchServiceClient.serviceName) as SearchServiceClient;
    const query_obj: Query = { semanticQuery: query };
    const _filters: Filters = { scope: [], userEmails: [], ...filters };
    const searchRequest: SearchChunksRequest = {
      query: query_obj,
      count,
      filters: filters ? _filters : undefined
    };

    const response = await new Promise<SearchChunksResponse>((resolve, reject) => {
      client.searchChunks(searchRequest, requestMetadata, (err, response) => {
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
   * Get chunks for a document via a specific reference
   * @param accessToken - The user's Redactive access token.
   * @param ref - A reference to the document to retrieve. Can be either a url or document name.
   * @param filters - The filters for querying documents. Optional. Only applicable for getting by document name.
   * @returns The complete list of chunks for the matching document.
   */
  async getDocument({
    accessToken,
    ref,
    filters
  }: GetDocumentParams): Promise<Chunk[]> {
    const requestMetadata = new Metadata();
    requestMetadata.set("Authorization", `Bearer ${accessToken}`);
    requestMetadata.set("User-Agent", "redactive-sdk-node");

    const client = this._getClient(SearchServiceClient.serviceName) as SearchServiceClient;
    const _filters: Filters = { scope: [], userEmails: [], ...filters };
    const queryRequest: GetDocumentRequest = {
      ref,
      filters: filters ? _filters : undefined
    };

    const response = await new Promise<GetDocumentResponse>((resolve, reject) => {
      client.getDocument(queryRequest, requestMetadata, (err, response) => {
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
