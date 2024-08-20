import { Client, credentials, Metadata } from "@grpc/grpc-js";

import { RelevantChunk } from "./grpc/chunks";
import { Query, QueryRequest, QueryResponse, SearchClient as SearchServiceClient } from "./grpc/search";

export class SearchClient {
  host: string = "grpc.redactive.ai";
  port: number = 443;
  _cachedServiceClients: Map<string, Client>;

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

  async queryChunks(accessToken: string, semanticQuery: string, count: number = 10): Promise<RelevantChunk[]> {
    const requestMetadata = new Metadata();
    requestMetadata.set("Authorization", `Bearer ${accessToken}`);
    requestMetadata.set("User-Agent", "redactive-sdk-node");

    const client = this._getClient(SearchServiceClient.serviceName) as SearchServiceClient;
    const query: Query = { semanticQuery };
    const queryRequest: QueryRequest = {
      query,
      count
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
}
