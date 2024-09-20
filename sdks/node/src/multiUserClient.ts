import { randomUUID } from "node:crypto";

import { AuthClient } from "./authClient";
import { Chunk, RelevantChunk } from "./grpc/chunks";
import { SearchClient } from "./searchClient";

export interface UserData {
  signInState?: string;
  refreshToken?: string;
  idToken?: string;
  idTokenExpiry?: Date;
  connections?: string[];
}

export class MultiUserClient {
  authClient: AuthClient;
  searchClient: SearchClient;

  callbackUri: string;

  readUserData: (userId: string) => Promise<UserData | undefined>;
  writeUserData: (userId: string, data: UserData | undefined) => Promise<void>;

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

  async getBeginConnectionUrl(userId: string, provider: string): Promise<string> {
    const state = randomUUID();
    const url = await this.authClient.beginConnection(provider, this.callbackUri, undefined, undefined, state);

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

  async handleConnectionCallback(userId: string, signInCode: string, state: string): Promise<boolean> {
    const userData = await this.readUserData(userId);
    if (!userData || !state || userData.signInState !== state) {
      return false;
    }
    await this._refreshUserData(userId, undefined, signInCode);
    return true;
  }

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

  async queryChunks(userId: string, semanticQuery: string, count: number = 10): Promise<RelevantChunk[]> {
    let userData = await this.readUserData(userId);
    if (!userData || !userData.refreshToken) {
      throw new Error(`No valid Redactive session for user '${userId}'`);
    }
    if (!!userData.idTokenExpiry && new Date(userData.idTokenExpiry) < new Date()) {
      userData = await this._refreshUserData(userId, userData.refreshToken, undefined);
    }

    return await this.searchClient.queryChunks(userData.idToken!, semanticQuery, count);
  }

  async getChunksByUrl(userId: string, url: string): Promise<Chunk[]> {
    let userData = await this.readUserData(userId);
    if (!userData || !userData.refreshToken) {
      throw new Error(`No valid Redactive session for user '${userId}'`);
    }
    if (!!userData.idTokenExpiry && new Date(userData.idTokenExpiry) < new Date()) {
      userData = await this._refreshUserData(userId, userData.refreshToken, undefined);
    }

    return await this.searchClient.getChunksByUrl(userData.idToken!, url);
  }
}
