// Code generated by protoc-gen-ts_proto. DO NOT EDIT.
// versions:
//   protoc-gen-ts_proto  v2.0.3
//   protoc               v5.27.3
// source: search.proto

/* eslint-disable */
import { BinaryReader, BinaryWriter } from "@bufbuild/protobuf/wire";
import {
  ChannelCredentials,
  Client,
  makeGenericClientConstructor,
  Metadata,
  type CallOptions,
  type ClientOptions,
  type ClientUnaryCall,
  type handleUnaryCall,
  type ServiceError,
  type UntypedServiceImplementation
} from "@grpc/grpc-js";

import { Chunk, RelevantChunk } from "./chunks";
import { Struct } from "./google/protobuf/struct";
import { Timestamp } from "./google/protobuf/timestamp";

export const protobufPackage = "redactive.grpc.v1";

export interface Query {
  /** Semantic query to execute */
  semanticQuery: string;
}

export interface TimeSpan {
  after?: Date | undefined;
  before?: Date | undefined;
}

export interface Filters {
  /** Scope e.g. "confluence", "slack://channel-name", "google-drive://CompanyDrive/document.docx" */
  scope: string[];
  /** Timespan of response chunk's creation */
  created?: TimeSpan | undefined;
  /** Timespan of response chunk's last modification */
  modified?: TimeSpan | undefined;
  /** List of user emails associated with response chunk */
  userEmails: string[];
  /** Include content from documents in trash */
  includeContentInTrash?: boolean | undefined;
}

export interface QueryRequest {
  /** How many results to try to return (maximum number of results) */
  count?: number | undefined;
  /** The query to execute */
  query: Query | undefined;
  /** Filters to apply to query */
  filters?: Filters | undefined;
}

export interface QueryResponse {
  /** Query was successful */
  success: boolean;
  /** Error message if query failed */
  error?: { [key: string]: any } | undefined;
  /** List of relevant chunks */
  relevantChunks: RelevantChunk[];
}

export interface GetChunksByUrlRequest {
  /** URL to document */
  url: string;
}

export interface GetChunksByUrlResponse {
  /** Fetch was successful */
  success: boolean;
  /** Error message if fetch failed */
  error?: { [key: string]: any } | undefined;
  /** List of chunks */
  chunks: Chunk[];
}

function createBaseQuery(): Query {
  return { semanticQuery: "" };
}

export const Query = {
  encode(message: Query, writer: BinaryWriter = new BinaryWriter()): BinaryWriter {
    if (message.semanticQuery !== "") {
      writer.uint32(10).string(message.semanticQuery);
    }
    return writer;
  },

  decode(input: BinaryReader | Uint8Array, length?: number): Query {
    const reader = input instanceof BinaryReader ? input : new BinaryReader(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseQuery();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.semanticQuery = reader.string();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skip(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Query {
    return { semanticQuery: isSet(object.semanticQuery) ? globalThis.String(object.semanticQuery) : "" };
  },

  toJSON(message: Query): unknown {
    const obj: any = {};
    if (message.semanticQuery !== "") {
      obj.semanticQuery = message.semanticQuery;
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<Query>, I>>(base?: I): Query {
    return Query.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<Query>, I>>(object: I): Query {
    const message = createBaseQuery();
    message.semanticQuery = object.semanticQuery ?? "";
    return message;
  }
};

function createBaseTimeSpan(): TimeSpan {
  return { after: undefined, before: undefined };
}

export const TimeSpan = {
  encode(message: TimeSpan, writer: BinaryWriter = new BinaryWriter()): BinaryWriter {
    if (message.after !== undefined) {
      Timestamp.encode(toTimestamp(message.after), writer.uint32(10).fork()).join();
    }
    if (message.before !== undefined) {
      Timestamp.encode(toTimestamp(message.before), writer.uint32(18).fork()).join();
    }
    return writer;
  },

  decode(input: BinaryReader | Uint8Array, length?: number): TimeSpan {
    const reader = input instanceof BinaryReader ? input : new BinaryReader(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseTimeSpan();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.after = fromTimestamp(Timestamp.decode(reader, reader.uint32()));
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.before = fromTimestamp(Timestamp.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skip(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): TimeSpan {
    return {
      after: isSet(object.after) ? fromJsonTimestamp(object.after) : undefined,
      before: isSet(object.before) ? fromJsonTimestamp(object.before) : undefined
    };
  },

  toJSON(message: TimeSpan): unknown {
    const obj: any = {};
    if (message.after !== undefined) {
      obj.after = message.after.toISOString();
    }
    if (message.before !== undefined) {
      obj.before = message.before.toISOString();
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<TimeSpan>, I>>(base?: I): TimeSpan {
    return TimeSpan.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<TimeSpan>, I>>(object: I): TimeSpan {
    const message = createBaseTimeSpan();
    message.after = object.after ?? undefined;
    message.before = object.before ?? undefined;
    return message;
  }
};

function createBaseFilters(): Filters {
  return { scope: [], created: undefined, modified: undefined, userEmails: [], includeContentInTrash: undefined };
}

export const Filters = {
  encode(message: Filters, writer: BinaryWriter = new BinaryWriter()): BinaryWriter {
    for (const v of message.scope) {
      writer.uint32(10).string(v!);
    }
    if (message.created !== undefined) {
      TimeSpan.encode(message.created, writer.uint32(18).fork()).join();
    }
    if (message.modified !== undefined) {
      TimeSpan.encode(message.modified, writer.uint32(26).fork()).join();
    }
    for (const v of message.userEmails) {
      writer.uint32(34).string(v!);
    }
    if (message.includeContentInTrash !== undefined) {
      writer.uint32(40).bool(message.includeContentInTrash);
    }
    return writer;
  },

  decode(input: BinaryReader | Uint8Array, length?: number): Filters {
    const reader = input instanceof BinaryReader ? input : new BinaryReader(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseFilters();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.scope.push(reader.string());
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.created = TimeSpan.decode(reader, reader.uint32());
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.modified = TimeSpan.decode(reader, reader.uint32());
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          message.userEmails.push(reader.string());
          continue;
        case 5:
          if (tag !== 40) {
            break;
          }

          message.includeContentInTrash = reader.bool();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skip(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Filters {
    return {
      scope: globalThis.Array.isArray(object?.scope) ? object.scope.map((e: any) => globalThis.String(e)) : [],
      created: isSet(object.created) ? TimeSpan.fromJSON(object.created) : undefined,
      modified: isSet(object.modified) ? TimeSpan.fromJSON(object.modified) : undefined,
      userEmails: globalThis.Array.isArray(object?.userEmails)
        ? object.userEmails.map((e: any) => globalThis.String(e))
        : [],
      includeContentInTrash: isSet(object.includeContentInTrash)
        ? globalThis.Boolean(object.includeContentInTrash)
        : undefined
    };
  },

  toJSON(message: Filters): unknown {
    const obj: any = {};
    if (message.scope?.length) {
      obj.scope = message.scope;
    }
    if (message.created !== undefined) {
      obj.created = TimeSpan.toJSON(message.created);
    }
    if (message.modified !== undefined) {
      obj.modified = TimeSpan.toJSON(message.modified);
    }
    if (message.userEmails?.length) {
      obj.userEmails = message.userEmails;
    }
    if (message.includeContentInTrash !== undefined) {
      obj.includeContentInTrash = message.includeContentInTrash;
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<Filters>, I>>(base?: I): Filters {
    return Filters.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<Filters>, I>>(object: I): Filters {
    const message = createBaseFilters();
    message.scope = object.scope?.map((e) => e) || [];
    message.created =
      object.created !== undefined && object.created !== null ? TimeSpan.fromPartial(object.created) : undefined;
    message.modified =
      object.modified !== undefined && object.modified !== null ? TimeSpan.fromPartial(object.modified) : undefined;
    message.userEmails = object.userEmails?.map((e) => e) || [];
    message.includeContentInTrash = object.includeContentInTrash ?? undefined;
    return message;
  }
};

function createBaseQueryRequest(): QueryRequest {
  return { count: undefined, query: undefined, filters: undefined };
}

export const QueryRequest = {
  encode(message: QueryRequest, writer: BinaryWriter = new BinaryWriter()): BinaryWriter {
    if (message.count !== undefined) {
      writer.uint32(8).uint32(message.count);
    }
    if (message.query !== undefined) {
      Query.encode(message.query, writer.uint32(18).fork()).join();
    }
    if (message.filters !== undefined) {
      Filters.encode(message.filters, writer.uint32(26).fork()).join();
    }
    return writer;
  },

  decode(input: BinaryReader | Uint8Array, length?: number): QueryRequest {
    const reader = input instanceof BinaryReader ? input : new BinaryReader(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseQueryRequest();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 8) {
            break;
          }

          message.count = reader.uint32();
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.query = Query.decode(reader, reader.uint32());
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.filters = Filters.decode(reader, reader.uint32());
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skip(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): QueryRequest {
    return {
      count: isSet(object.count) ? globalThis.Number(object.count) : undefined,
      query: isSet(object.query) ? Query.fromJSON(object.query) : undefined,
      filters: isSet(object.filters) ? Filters.fromJSON(object.filters) : undefined
    };
  },

  toJSON(message: QueryRequest): unknown {
    const obj: any = {};
    if (message.count !== undefined) {
      obj.count = Math.round(message.count);
    }
    if (message.query !== undefined) {
      obj.query = Query.toJSON(message.query);
    }
    if (message.filters !== undefined) {
      obj.filters = Filters.toJSON(message.filters);
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<QueryRequest>, I>>(base?: I): QueryRequest {
    return QueryRequest.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<QueryRequest>, I>>(object: I): QueryRequest {
    const message = createBaseQueryRequest();
    message.count = object.count ?? undefined;
    message.query = object.query !== undefined && object.query !== null ? Query.fromPartial(object.query) : undefined;
    message.filters =
      object.filters !== undefined && object.filters !== null ? Filters.fromPartial(object.filters) : undefined;
    return message;
  }
};

function createBaseQueryResponse(): QueryResponse {
  return { success: false, error: undefined, relevantChunks: [] };
}

export const QueryResponse = {
  encode(message: QueryResponse, writer: BinaryWriter = new BinaryWriter()): BinaryWriter {
    if (message.success !== false) {
      writer.uint32(8).bool(message.success);
    }
    if (message.error !== undefined) {
      Struct.encode(Struct.wrap(message.error), writer.uint32(18).fork()).join();
    }
    for (const v of message.relevantChunks) {
      RelevantChunk.encode(v!, writer.uint32(26).fork()).join();
    }
    return writer;
  },

  decode(input: BinaryReader | Uint8Array, length?: number): QueryResponse {
    const reader = input instanceof BinaryReader ? input : new BinaryReader(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseQueryResponse();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 8) {
            break;
          }

          message.success = reader.bool();
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.error = Struct.unwrap(Struct.decode(reader, reader.uint32()));
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.relevantChunks.push(RelevantChunk.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skip(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): QueryResponse {
    return {
      success: isSet(object.success) ? globalThis.Boolean(object.success) : false,
      error: isObject(object.error) ? object.error : undefined,
      relevantChunks: globalThis.Array.isArray(object?.relevantChunks)
        ? object.relevantChunks.map((e: any) => RelevantChunk.fromJSON(e))
        : []
    };
  },

  toJSON(message: QueryResponse): unknown {
    const obj: any = {};
    if (message.success !== false) {
      obj.success = message.success;
    }
    if (message.error !== undefined) {
      obj.error = message.error;
    }
    if (message.relevantChunks?.length) {
      obj.relevantChunks = message.relevantChunks.map((e) => RelevantChunk.toJSON(e));
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<QueryResponse>, I>>(base?: I): QueryResponse {
    return QueryResponse.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<QueryResponse>, I>>(object: I): QueryResponse {
    const message = createBaseQueryResponse();
    message.success = object.success ?? false;
    message.error = object.error ?? undefined;
    message.relevantChunks = object.relevantChunks?.map((e) => RelevantChunk.fromPartial(e)) || [];
    return message;
  }
};

function createBaseGetChunksByUrlRequest(): GetChunksByUrlRequest {
  return { url: "" };
}

export const GetChunksByUrlRequest = {
  encode(message: GetChunksByUrlRequest, writer: BinaryWriter = new BinaryWriter()): BinaryWriter {
    if (message.url !== "") {
      writer.uint32(10).string(message.url);
    }
    return writer;
  },

  decode(input: BinaryReader | Uint8Array, length?: number): GetChunksByUrlRequest {
    const reader = input instanceof BinaryReader ? input : new BinaryReader(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseGetChunksByUrlRequest();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.url = reader.string();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skip(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): GetChunksByUrlRequest {
    return { url: isSet(object.url) ? globalThis.String(object.url) : "" };
  },

  toJSON(message: GetChunksByUrlRequest): unknown {
    const obj: any = {};
    if (message.url !== "") {
      obj.url = message.url;
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<GetChunksByUrlRequest>, I>>(base?: I): GetChunksByUrlRequest {
    return GetChunksByUrlRequest.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<GetChunksByUrlRequest>, I>>(object: I): GetChunksByUrlRequest {
    const message = createBaseGetChunksByUrlRequest();
    message.url = object.url ?? "";
    return message;
  }
};

function createBaseGetChunksByUrlResponse(): GetChunksByUrlResponse {
  return { success: false, error: undefined, chunks: [] };
}

export const GetChunksByUrlResponse = {
  encode(message: GetChunksByUrlResponse, writer: BinaryWriter = new BinaryWriter()): BinaryWriter {
    if (message.success !== false) {
      writer.uint32(8).bool(message.success);
    }
    if (message.error !== undefined) {
      Struct.encode(Struct.wrap(message.error), writer.uint32(18).fork()).join();
    }
    for (const v of message.chunks) {
      Chunk.encode(v!, writer.uint32(26).fork()).join();
    }
    return writer;
  },

  decode(input: BinaryReader | Uint8Array, length?: number): GetChunksByUrlResponse {
    const reader = input instanceof BinaryReader ? input : new BinaryReader(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseGetChunksByUrlResponse();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 8) {
            break;
          }

          message.success = reader.bool();
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.error = Struct.unwrap(Struct.decode(reader, reader.uint32()));
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.chunks.push(Chunk.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skip(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): GetChunksByUrlResponse {
    return {
      success: isSet(object.success) ? globalThis.Boolean(object.success) : false,
      error: isObject(object.error) ? object.error : undefined,
      chunks: globalThis.Array.isArray(object?.chunks) ? object.chunks.map((e: any) => Chunk.fromJSON(e)) : []
    };
  },

  toJSON(message: GetChunksByUrlResponse): unknown {
    const obj: any = {};
    if (message.success !== false) {
      obj.success = message.success;
    }
    if (message.error !== undefined) {
      obj.error = message.error;
    }
    if (message.chunks?.length) {
      obj.chunks = message.chunks.map((e) => Chunk.toJSON(e));
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<GetChunksByUrlResponse>, I>>(base?: I): GetChunksByUrlResponse {
    return GetChunksByUrlResponse.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<GetChunksByUrlResponse>, I>>(object: I): GetChunksByUrlResponse {
    const message = createBaseGetChunksByUrlResponse();
    message.success = object.success ?? false;
    message.error = object.error ?? undefined;
    message.chunks = object.chunks?.map((e) => Chunk.fromPartial(e)) || [];
    return message;
  }
};

export type SearchService = typeof SearchService;
export const SearchService = {
  /** Query the index for relevant chunks */
  queryChunks: {
    path: "/redactive.grpc.v1.Search/QueryChunks",
    requestStream: false,
    responseStream: false,
    requestSerialize: (value: QueryRequest) => Buffer.from(QueryRequest.encode(value).finish()),
    requestDeserialize: (value: Buffer) => QueryRequest.decode(value),
    responseSerialize: (value: QueryResponse) => Buffer.from(QueryResponse.encode(value).finish()),
    responseDeserialize: (value: Buffer) => QueryResponse.decode(value)
  },
  /** Get chunks by URL */
  getChunksByUrl: {
    path: "/redactive.grpc.v1.Search/GetChunksByUrl",
    requestStream: false,
    responseStream: false,
    requestSerialize: (value: GetChunksByUrlRequest) => Buffer.from(GetChunksByUrlRequest.encode(value).finish()),
    requestDeserialize: (value: Buffer) => GetChunksByUrlRequest.decode(value),
    responseSerialize: (value: GetChunksByUrlResponse) => Buffer.from(GetChunksByUrlResponse.encode(value).finish()),
    responseDeserialize: (value: Buffer) => GetChunksByUrlResponse.decode(value)
  }
} as const;

export interface SearchServer extends UntypedServiceImplementation {
  /** Query the index for relevant chunks */
  queryChunks: handleUnaryCall<QueryRequest, QueryResponse>;
  /** Get chunks by URL */
  getChunksByUrl: handleUnaryCall<GetChunksByUrlRequest, GetChunksByUrlResponse>;
}

export interface SearchClient extends Client {
  /** Query the index for relevant chunks */
  queryChunks(
    request: QueryRequest,
    callback: (error: ServiceError | null, response: QueryResponse) => void
  ): ClientUnaryCall;
  queryChunks(
    request: QueryRequest,
    metadata: Metadata,
    callback: (error: ServiceError | null, response: QueryResponse) => void
  ): ClientUnaryCall;
  queryChunks(
    request: QueryRequest,
    metadata: Metadata,
    options: Partial<CallOptions>,
    callback: (error: ServiceError | null, response: QueryResponse) => void
  ): ClientUnaryCall;
  /** Get chunks by URL */
  getChunksByUrl(
    request: GetChunksByUrlRequest,
    callback: (error: ServiceError | null, response: GetChunksByUrlResponse) => void
  ): ClientUnaryCall;
  getChunksByUrl(
    request: GetChunksByUrlRequest,
    metadata: Metadata,
    callback: (error: ServiceError | null, response: GetChunksByUrlResponse) => void
  ): ClientUnaryCall;
  getChunksByUrl(
    request: GetChunksByUrlRequest,
    metadata: Metadata,
    options: Partial<CallOptions>,
    callback: (error: ServiceError | null, response: GetChunksByUrlResponse) => void
  ): ClientUnaryCall;
}

export const SearchClient = makeGenericClientConstructor(SearchService, "redactive.grpc.v1.Search") as unknown as {
  new (address: string, credentials: ChannelCredentials, options?: Partial<ClientOptions>): SearchClient;
  service: typeof SearchService;
  serviceName: string;
};

type Builtin = Date | Function | Uint8Array | string | number | boolean | undefined;

export type DeepPartial<T> = T extends Builtin
  ? T
  : T extends globalThis.Array<infer U>
    ? globalThis.Array<DeepPartial<U>>
    : T extends ReadonlyArray<infer U>
      ? ReadonlyArray<DeepPartial<U>>
      : T extends {}
        ? { [K in keyof T]?: DeepPartial<T[K]> }
        : Partial<T>;

type KeysOfUnion<T> = T extends T ? keyof T : never;
export type Exact<P, I extends P> = P extends Builtin
  ? P
  : P & { [K in keyof P]: Exact<P[K], I[K]> } & { [K in Exclude<keyof I, KeysOfUnion<P>>]: never };

function toTimestamp(date: Date): Timestamp {
  const seconds = Math.trunc(date.getTime() / 1_000);
  const nanos = (date.getTime() % 1_000) * 1_000_000;
  return { seconds, nanos };
}

function fromTimestamp(t: Timestamp): Date {
  let millis = (t.seconds || 0) * 1_000;
  millis += (t.nanos || 0) / 1_000_000;
  return new globalThis.Date(millis);
}

function fromJsonTimestamp(o: any): Date {
  if (o instanceof globalThis.Date) {
    return o;
  } else if (typeof o === "string") {
    return new globalThis.Date(o);
  } else {
    return fromTimestamp(Timestamp.fromJSON(o));
  }
}

function isObject(value: any): boolean {
  return typeof value === "object" && value !== null;
}

function isSet(value: any): boolean {
  return value !== null && value !== undefined;
}
