import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { AuthClient } from "./authClient";

describe("API client", () => {
  const originFetch = global.fetch;

  beforeEach(() => {
    global.fetch = vi.fn().mockResolvedValue({
      json: () => Promise.resolve({})
    });
  });

  afterEach(() => {
    global.fetch = originFetch;
  });

  it("should start connection to data source", async () => {
    const apiKey = "test-apiKey";
    const provider = "test-confluence";
    const redirectUri = "https://mock.api";
    const expectedResponse = "https://confluence.mock.api";

    // Mocking fetch response for beginConnection
    // eslint-disable-next-line
    (fetch as any).mockResolvedValue({
      json: () => Promise.resolve({ url: expectedResponse })
    });

    const client = new AuthClient(apiKey);
    const response = await client.beginConnection(provider, redirectUri);

    // Assertions
    expect(fetch).toHaveBeenCalledWith(
      `https://api.redactive.ai/api/auth/connect/${provider}/url?redirect_uri=${encodeURIComponent(redirectUri)}`,
      {
        method: "POST",
        headers: new Headers({
          "User-Agent": "redactive-sdk-node",
          "Content-Type": "application/json",
          Authorization: `Bearer ${apiKey}`
        })
      }
    );
    expect(response).toBe(expectedResponse);
  });

  it("should exchange token", async () => {
    const apiKey = "test-apiKey";
    const code = "test-code";
    const refreshToken = "test-refreshToken";
    const expectedResponse = {
      idToken: "test-idToken",
      refreshToken: "test-refreshToken",
      expiresIn: 3600
    };

    // Mocking fetch response for exchangeTokens
    // eslint-disable-next-line
    (fetch as any).mockResolvedValue({
      json: () => Promise.resolve(expectedResponse)
    });

    const client = new AuthClient(apiKey);
    const response = await client.exchangeTokens(code, refreshToken);

    // Assertions
    expect(fetch).toHaveBeenCalledWith("https://api.redactive.ai/api/auth/token", {
      method: "POST",
      headers: new Headers({
        "User-Agent": "redactive-sdk-node",
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`
      }),
      body: JSON.stringify({ code, refresh_token: refreshToken })
    });
    expect(response).toEqual(expectedResponse);
  });

  it("should list connections", async () => {
    const apiKey = "test-apiKey";
    const accessToken = "test-access-token";
    const expectedResponse = {
      user_id: "test-user",
      current_connections: ["confluence"]
    };

    // Mocking fetch response for listConnections
    // eslint-disable-next-line
    (fetch as any).mockResolvedValue({
      json: () => Promise.resolve(expectedResponse)
    });

    const client = new AuthClient(apiKey);
    const response = await client.listConnections(accessToken);

    // Assertions
    expect(fetch).toHaveBeenCalledWith("https://api.redactive.ai/api/auth/connections", {
      method: "GET",
      headers: new Headers({
        "User-Agent": "redactive-sdk-node",
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`
      })
    });
    expect(response).toEqual({
      userId: expectedResponse.user_id,
      connections: expectedResponse.current_connections
    });
  });

  it("should list connections", async () => {
    const apiKey = "test-apiKey";
    const accessToken = "test-access-token";
    const expectedResponse = {
      user_id: "test-user",
      current_connections: ["confluence"]
    };

    // Mocking fetch response for listConnections
    // eslint-disable-next-line
    (fetch as any).mockResolvedValue({
      json: () => Promise.resolve(expectedResponse)
    });

    const client = new AuthClient(apiKey);
    const response = await client.listConnections(accessToken);

    // Assertions
    expect(fetch).toHaveBeenCalledWith("https://api.redactive.ai/api/auth/connections", {
      method: "GET",
      headers: new Headers({
        "User-Agent": "redactive-sdk-node",
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`
      })
    });
    expect(response).toEqual({
      userId: expectedResponse.user_id,
      connections: expectedResponse.current_connections
    });
  });
});
