import { randomUUID } from "crypto";

import { beforeEach, describe, expect, it, Mock, Mocked, MockedFunction, vi } from "vitest";

import { AuthClient } from "./authClient";
import { Chunk, RelevantChunk } from "./grpc/chunks";
import { MultiUserClient, UserData } from "./multiUserClient";
import { SearchClient } from "./searchClient";

vi.mock("./authClient");
vi.mock("./searchClient");
vi.mock("crypto", () => ({
  randomUUID: vi.fn()
}));

describe("MultiUserClient", () => {
  let multiUserClient: MultiUserClient;
  let mockAuthClient: Mocked<AuthClient>;
  let mockSearchClient: Mocked<SearchClient>;
  let readUserData: MockedFunction<(userId: string) => Promise<UserData | undefined>>;
  let writeUserData: MockedFunction<(userId: string, data: UserData | undefined) => Promise<void>>;

  beforeEach(() => {
    mockAuthClient = new AuthClient("test-apiKey") as Mocked<AuthClient>;
    mockSearchClient = new SearchClient() as Mocked<SearchClient>;
    readUserData = vi.fn();
    writeUserData = vi.fn();
    multiUserClient = new MultiUserClient("apiKey", "http://callback.uri", readUserData, writeUserData);
  });

  it("should generate a connection URL and save the state", async () => {
    const userId = "user123";
    const provider = "google";
    const state = "state123";
    const url = "http://auth.url";

    (randomUUID as Mock).mockReturnValue(state);
    mockAuthClient.beginConnection.mockResolvedValue(url);
    readUserData.mockResolvedValue({});

    multiUserClient.authClient = mockAuthClient;
    const result = await multiUserClient.getBeginConnectionUrl(userId, provider);

    expect(result).toBe(url);
    expect(mockAuthClient.beginConnection).toHaveBeenCalledWith({
      provider,
      redirectUri: "http://callback.uri",
      state
    });
    expect(writeUserData).toHaveBeenCalledWith(userId, { signInState: state });
  });

  it("should refresh user data using refresh token", async () => {
    const userId = "user123";
    const refreshToken = "refreshToken123";
    const idToken = "idToken123";
    const expiresIn = 3600;
    const connections = ["conn1", "conn2"];

    mockAuthClient.exchangeTokens.mockResolvedValue({
      idToken,
      refreshToken,
      expiresIn
    });
    mockAuthClient.listConnections.mockResolvedValue({ userId, connections });

    multiUserClient.authClient = mockAuthClient;
    const userData = await multiUserClient._refreshUserData(userId, refreshToken);

    expect(userData).toEqual({
      refreshToken,
      idToken,
      idTokenExpiry: expect.any(Date),
      connections
    });
    expect(mockAuthClient.exchangeTokens).toHaveBeenCalledWith(undefined, refreshToken);
    expect(mockAuthClient.listConnections).toHaveBeenCalledWith(idToken);
    expect(writeUserData).toHaveBeenCalledWith(userId, {
      refreshToken,
      idToken,
      idTokenExpiry: expect.any(Date),
      connections
    });
  });

  it("should retrieve user email from idToken", async () => {
    const userId = "user123";
    const email = "user@example.com";
    const idToken = `header.${btoa(JSON.stringify({ email }))}.signature`;

    readUserData.mockResolvedValue({ idToken });

    const result = await multiUserClient.getUsersRedactiveEmail(userId);

    expect(result).toBe(email);
  });

  it("should handle connection callback successfully", async () => {
    const userId = "user123";
    const signInCode = "code123";
    const state = "state123";
    const userData: UserData = { signInState: state };

    readUserData.mockResolvedValue(userData);

    multiUserClient.readUserData = readUserData;
    multiUserClient._refreshUserData = vi.fn();
    const result = await multiUserClient.handleConnectionCallback(userId, signInCode, state);

    expect(result).toBe(true);
    expect(multiUserClient._refreshUserData).toHaveBeenCalledWith(userId, undefined, signInCode);
  });

  it("should return user connections if idToken is valid", async () => {
    const userId = "user123";
    const connections = ["conn1", "conn2"];
    const userData: UserData = {
      idToken: "idToken123",
      idTokenExpiry: new Date(Date.now() + 3600 * 1000),
      connections
    };

    readUserData.mockResolvedValue(userData);

    const result = await multiUserClient.getUserConnections(userId);

    expect(result).toEqual(connections);
  });

  it("should clear user data", async () => {
    const userId = "user123";

    await multiUserClient.clearUserData(userId);

    expect(writeUserData).toHaveBeenCalledWith(userId, undefined);
  });

  it("should throw an error if no valid session when querying chunks", async () => {
    const userId = "user123";
    const semanticQuery = "query";

    readUserData.mockResolvedValue(undefined);

    await expect(multiUserClient.queryChunks({ userId, semanticQuery })).rejects.toThrow(
      `No valid Redactive session for user '${userId}'`
    );
  });

  it("should query chunks after refreshing idToken", async () => {
    const userId = "user123";
    const semanticQuery = "query";
    const idToken = "idToken123";
    const refreshToken = "refreshToken123";
    const chunks = [{ chunk: "chunk1" }, { chunk: "chunk2" }];

    const expiredUserData: UserData = {
      idToken,
      idTokenExpiry: new Date(Date.now() - 1000),
      refreshToken
    };
    const refreshedUserData: UserData = {
      idToken,
      idTokenExpiry: new Date(Date.now() + 3600 * 1000),
      refreshToken
    };

    readUserData.mockResolvedValueOnce(expiredUserData).mockResolvedValueOnce(refreshedUserData);
    multiUserClient._refreshUserData = vi.fn().mockResolvedValue(refreshedUserData);
    mockSearchClient.queryChunks.mockResolvedValue(chunks as unknown as RelevantChunk[]);

    multiUserClient.searchClient = mockSearchClient;
    const result = await multiUserClient.queryChunks({ userId, semanticQuery });

    expect(result).toEqual(chunks);
    expect(mockSearchClient.queryChunks).toHaveBeenCalledWith({ accessToken: idToken, semanticQuery, count: 10 });
  });

  it("should query chunks by document name after refreshing idToken", async () => {
    const userId = "user123";
    const documentName = "test-document";
    const idToken = "idToken123";
    const refreshToken = "refreshToken123";
    const chunks = [{ chunk: "chunk1" }, { chunk: "chunk2" }];

    const expiredUserData: UserData = {
      idToken,
      idTokenExpiry: new Date(Date.now() - 1000),
      refreshToken
    };
    const refreshedUserData: UserData = {
      idToken,
      idTokenExpiry: new Date(Date.now() + 3600 * 1000),
      refreshToken
    };

    readUserData.mockResolvedValueOnce(expiredUserData).mockResolvedValueOnce(refreshedUserData);
    multiUserClient._refreshUserData = vi.fn().mockResolvedValue(refreshedUserData);
    mockSearchClient.queryChunksByDocumentName.mockResolvedValue(chunks as unknown as Chunk[]);

    multiUserClient.searchClient = mockSearchClient;
    const result = await multiUserClient.queryChunksByDocumentName({ userId, documentName });

    expect(result).toEqual(chunks);
    expect(mockSearchClient.queryChunksByDocumentName).toHaveBeenCalledWith({ accessToken: idToken, documentName });
  });

  it("should get chunks by url after refreshing idToken", async () => {
    const userId = "user123";
    const url = "https://example.com";
    const idToken = "idToken123";
    const refreshToken = "refreshToken123";
    const chunks = [{ chunk: "chunk1" }, { chunk: "chunk2" }];

    const expiredUserData: UserData = {
      idToken,
      idTokenExpiry: new Date(Date.now() - 1000),
      refreshToken
    };
    const refreshedUserData: UserData = {
      idToken,
      idTokenExpiry: new Date(Date.now() + 3600 * 1000),
      refreshToken
    };

    readUserData.mockResolvedValueOnce(expiredUserData).mockResolvedValueOnce(refreshedUserData);
    multiUserClient._refreshUserData = vi.fn().mockResolvedValue(refreshedUserData);
    mockSearchClient.getChunksByUrl.mockResolvedValue(chunks as unknown as Chunk[]);

    multiUserClient.searchClient = mockSearchClient;
    const result = await multiUserClient.getChunksByUrl({ userId, url });

    expect(result).toEqual(chunks);
    expect(mockSearchClient.getChunksByUrl).toHaveBeenCalledWith({ accessToken: idToken, url });
  });
});
