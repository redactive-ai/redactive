import { randomUUID } from "node:crypto";

import { AuthClient } from "./authClient";
import { Chunk, RelevantChunk } from "./grpc/chunks";
import { GetDocumentParams, SearchChunksParams, SearchClient } from "./searchClient";

export interface UserData {
  signInState?: string;
  refreshToken?: string;
  idToken?: string;
  idTokenExpiry?: Date;
  connections?: string[];
}

export interface MultiUserSearchChunksParams extends Omit<SearchChunksParams, "accessToken"> {
  userId: string;
}

export interface MultiUserGetDocumentParams extends Omit<GetDocumentParams, "accessToken"> {
  userId: string;
}

export class MultiUserClient {
  authClient: AuthClient;
  searchClient: SearchClient;

  callbackUri: string;

  readUserData: (userId: string) => Promise<UserData | undefined>;
  writeUserData: (userId: string, data: UserData | undefined) => Promise<void>;

  /**
   * Redactive client handling multiple user authentication and access to the Redactive Search service.
   * @param apiKey - Redactive API key.
   * @param callbackUri - The URI to redirect to after initiating the connection.
   * @param readUserData - Function to read user data from storage.
   * @param writeUserData - Function to write user data to storage.
   * @param options - An object of client options. Optional.
   * @param options.authBaseUrl - Base URL for the authentication service. Optional.
   * @param options.grpcHost - Host for the Redactive API service. Optional.
   * @param options.grpcPort - Port for the Redactive API service. Optional.
   */
  constructor(
    apiKey: string,
    callbackUri: string,
    readUserData: (userId: string) => Promise<UserData | undefined>,
    writeUserData: (userId: string, userData: UserData | undefined) => Promise<void>,
    options?: {
      authBaseUrl?: string;
      grpcHost?: string;
      grpcPort?: number;
    }
  ) {
    this.authClient = new AuthClient(apiKey, options?.authBaseUrl);
    this.searchClient = new SearchClient(options?.grpcHost, options?.grpcPort);

    this.callbackUri = callbackUri;

    this.readUserData = readUserData;
    this.writeUserData = writeUserData;
  }

  /**
   * Return a URL for authorizing Redactive to connect with provider on a user's behalf.
   * @param userId - A user ID to associate the connection URL with.
   * @param provider - The name of the provider to connect with.
   * @returns The URL to redirect the user to for beginning the connection.
   */
  async getBeginConnectionUrl(userId: string, provider: string): Promise<string> {
    const state = randomUUID();
    const url = await this.authClient.beginConnection({ provider, redirectUri: this.callbackUri, state });

    const userData = await this.readUserData(userId);
    await this.writeUserData(userId, {
      ...userData,
      signInState: state
    });
    return url;
  }

  _refreshUserData: (userId: string, refreshToken?: string, signInCode?: string) => Promise<UserData> = async (
    userId: string,
    refreshToken?: string,
    signInCode?: string
  ) => {
    const tokens = await this.authClient.exchangeTokens(signInCode, refreshToken);
    const connections = await this.authClient.listConnections(tokens.idToken);
    const userData = {
      refreshToken: tokens.refreshToken,
      idToken: tokens.idToken,
      idTokenExpiry: new Date(Date.now() + (tokens.expiresIn - 10) * 1000),
      connections: connections.connections
    };
    await this.writeUserData(userId, userData);
    return userData;
  };

  async getUsersRedactiveEmail(userId: string): Promise<string | undefined> {
    const userData = await this.readUserData(userId);
    if (!userData || !userData.idToken) {
      return undefined;
    }
    const encodedBody = userData.idToken.split(".")[1];
    const tokenBody = JSON.parse(atob(encodedBody));
    return tokenBody.email;
  }

  /**
   * The callback method for users completing the connection flow; to be called when user returns to app with
   * connection-related URL query parameters.
   * @param userId - The ID of the user completing their connection flow.
   * @param signInCode - The connection sign-in code returned in the URL query parameters by completing the connection flow.
   * @param state - The state value returned in the URL query parameters by completing the connection flow.
   * @returns A boolean representing successful connection completion.
   */
  async handleConnectionCallback(userId: string, signInCode: string, state: string): Promise<boolean> {
    const userData = await this.readUserData(userId);
    if (!userData || !state || userData.signInState !== state) {
      return false;
    }
    await this._refreshUserData(userId, undefined, signInCode);
    return true;
  }

  /**
   * Retrieve the list of the user's provider connections.
   * @param userId - The ID of the user.
   * @returns A list of the user's connected providers.
   */
  async getUserConnections(userId: string): Promise<string[]> {
    let userData = await this.readUserData(userId);
    if (!!userData && !!userData.idTokenExpiry && new Date(userData.idTokenExpiry) > new Date()) {
      return userData.connections ?? [];
    }
    if (!!userData && !!userData.refreshToken) {
      userData = await this._refreshUserData(userId, userData.refreshToken, undefined);
      return userData.connections ?? [];
    }
    return [];
  }

  async clearUserData(userId: string): Promise<void> {
    await this.writeUserData(userId, undefined);
  }

  /**
   * Query for relevant chunks based on a semantic query.
   * @param userId - The ID of the user.
   * @param query - The query string used to find relevant chunks.
   * @param count - The number of relevant chunks to retrieve. Defaults to 10.
   * @param filters - An object of filters for querying. Optional.
   * @returns list of relevant chunks.
   */
  async searchChunks({ userId, query, count = 10, filters }: MultiUserSearchChunksParams): Promise<RelevantChunk[]> {
    let userData = await this.readUserData(userId);
    if (!userData || !userData.refreshToken) {
      throw new Error(`No valid Redactive session for user '${userId}'`);
    }
    if (!!userData.idTokenExpiry && new Date(userData.idTokenExpiry) < new Date()) {
      userData = await this._refreshUserData(userId, userData.refreshToken, undefined);
    }

    return await this.searchClient.searchChunks({ accessToken: userData.idToken!, query, count, filters });
  }

  /**
   * Get chunks from a document by its URL.
   * @param accessToken - The user's Redactive access token.
   * @param ref - A reference to the document we are retrieving. Can be either a url or document name.
   * @param filters - The filters for querying documents. Optional. Only applicable for getting by document name.
   * @returns The complete list of chunks for the matching document.
   */
  async getDocument({ userId, ref, filters }: MultiUserGetDocumentParams): Promise<Chunk[]> {
    let userData = await this.readUserData(userId);
    if (!userData || !userData.refreshToken) {
      throw new Error(`No valid Redactive session for user '${userId}'`);
    }
    if (!!userData.idTokenExpiry && new Date(userData.idTokenExpiry) < new Date()) {
      userData = await this._refreshUserData(userId, userData.refreshToken, undefined);
    }

    return await this.searchClient.getDocument({ accessToken: userData.idToken!, ref, filters });
  }
}
