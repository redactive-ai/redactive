export interface ExchangeTokenResponse {
  idToken: string;
  refreshToken: string;
  expiresIn: number;
}

export interface UserConnections {
  userId: string;
  connections: string[];
}

export interface BeginConnectionParams {
  provider: string;
  redirectUri: string;
  endpoint?: string;
  codeParamAlias?: string;
  state?: string;
}

export class AuthClient {
  _requestHeaders: Headers;
  apiKey: string;
  baseUrl: string = "https://api.redactive.ai";

  /**
   * Initialize the connection settings for the Redactive API.
   * @param apiKey - The API key used for authentication.
   * @param baseUrl - The base URL to the Redactive API.
   */
  constructor(apiKey: string, baseUrl?: string) {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl || this.baseUrl;
    this._requestHeaders = new Headers({
      "User-Agent": "redactive-sdk-node",
      "Content-Type": "application/json",
      Authorization: `Bearer ${this.apiKey}`
    });
  }

  /**
   * Return a URL for authorizing Redactive to connect with provider on a user's behalf.
   * @param provider - The name of the provider to connect with.
   * @param redirectUri - THE URI to redirect to after initiating the connection. Defaults to an empty string.
   * @param endpoint - The endpoint to use to access specific provider APIs. Only required if connecting to Zendesk. Defaults to None.
   * @param codeParamAlias - The alias for the code parameter. This is the name of the query parameter that will need to be passed to the `/auth/token` endpoint as `code`. Defaults to None and will be `code` on the return.
   * @param state - An optional parameter that is stored as app_callback_state for building callback url. Defaults to None.
   * @returns The URL to redirect the user to for beginning the connection.
   */
  async beginConnection({
    provider,
    redirectUri,
    endpoint,
    codeParamAlias,
    state
  }: BeginConnectionParams): Promise<string> {
    const params = [`redirect_uri=${encodeURIComponent(redirectUri)}`];
    if (endpoint) {
      params.push(`endpoint=${encodeURIComponent(endpoint)}`);
    }
    if (state) {
      params.push(`state=${encodeURIComponent(state)}`);
    }
    if (codeParamAlias) {
      params.push(`code_param_alias=${encodeURIComponent(codeParamAlias)}`);
    }

    const response = await fetch(`${this.baseUrl}/api/auth/connect/${provider}/url?${params.join("&")}`, {
      method: "POST",
      headers: this._requestHeaders
    });

    return response.json().then((data) => data.url);
  }

  /**
   * Exchange an authorization code and refresh token for access tokens.
   * @param code - The authorization code received from the OAuth flow. Defaults to None.
   * @param refreshToken - The refresh token used for token refreshing. Defaults to None.
   * @returns an object containing access token and other token information.
   */
  async exchangeTokens(code?: string, refreshToken?: string): Promise<ExchangeTokenResponse> {
    if (!(code || refreshToken)) {
      throw Error("Missing required data");
    }
    const data = JSON.stringify({
      code,
      refresh_token: refreshToken
    });
    const response = await fetch(`${this.baseUrl}/api/auth/token`, {
      method: "POST",
      body: data,
      headers: this._requestHeaders
    });

    const result = await response.json();
    return result as ExchangeTokenResponse;
  }

  /**
   * Retrieve the list of user's provider connections.
   * @param accessToken - the user's access token for authentication.
   * @returns an object container the user ID and current provider connections.
   */
  async listConnections(accessToken: string): Promise<UserConnections> {
    const response = await fetch(`${this.baseUrl}/api/auth/connections`, {
      method: "GET",
      headers: new Headers({
        "User-Agent": "redactive-sdk-node",
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`
      })
    });

    const result = await response.json();
    return {
      userId: result.user_id,
      connections: result.current_connections
    } as UserConnections;
  }
}
