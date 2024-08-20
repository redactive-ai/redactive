export interface ExchangeTokenResponse {
  idToken: string;
  refreshToken: string;
  expiresIn: number;
}

export interface UserConnections {
  userId: string;
  connections: string[];
}

export class AuthClient {
  _requestHeaders: Headers;
  apiKey: string;
  baseUrl: string = "https://api.redactive.ai";

  constructor(apiKey: string, baseUrl?: string) {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl || this.baseUrl;
    this._requestHeaders = new Headers({
      "User-Agent": "redactive-sdk-node",
      "Content-Type": "application/json",
      Authorization: `Bearer ${this.apiKey}`
    });
  }

  async beginConnection(
    provider: string,
    redirectUri: string,
    endpoint?: string,
    codeParamAlias?: string,
    state?: string
  ): Promise<string> {
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
