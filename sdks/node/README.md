# Redactive Node SDK

The Redactive Node SDK provides a robust and intuitive interface for interacting with the Redactive platform, enabling developers to seamlessly integrate powerful data redaction and anonymization capabilities into their Node applications.

## Installation

In order to use the package to integrate with Redactive.ai, run:

```sh
npm install redactive
```

There is no need to clone this repository.

If you would like to modify this package, clone the repo and install from source:

```sh
npm install ./sdks/node
```

### Requirements

- Node v20+

## Usage

The library has following components.

- **AuthClient** - provides functionality to interact with data sources
- **SearchClient** - provides functionality to search chunks with Redactive search service in gRPC
- **MultiUserClient** - provides functionality manage multi-user search with Redactive search service

### AuthClient

AuthClient needs to be configured with your account's API key which is
available in the Apps page at [Redactive Dashboard](https://dashboard.redactive.ai/).

```javascript
import { AuthClient } from "@redactive/redactive";

// Establish an connection to data source
// Possible data sources: confluence, google-drive, jira, zendesk, slack, sharepoint
const redirectUri = "https://url-debugger.vercel.app";
const provider = "confluence";
const signInUrl = await client.beginConnection({ provider, redirectUri });

// Navigate User to signInUrl
// User will receive an oauth2 auth code after consenting the app's data source access permissions.
// Use this code to exchange Redactive access_token with Redactive API
const response = await client.exchangeTokens("OAUTH2-AUTH-CODE");
```

### SearchClient

With the Redactive access_token, you can perform three types of searches using the Redactive Search service:

1. **Semantic Query Search**: Retrieve relevant chunks of information that are semantically related to a user query.
2. **URL-based Search**: Obtain all the chunks from a document by specifying its URL.
3. **Document Name Search**: Query for all the chunks from a document based on the name of the document.

```javascript
import { SearchClient } from "@redactive/redactive";

const client = new SearchClient();
const accessToken = "REDACTIVE-ACCESS-TOKEN";

// Semantic Search: retrieve text extracts (chunks) from various documents pertaining to the user query
const semanticQuery = "Tell me about AI";
await client.queryChunks({ accessToken, semanticQuery });

// URL-based Search: retrieve all chunks of the document at that URL
const url = "https://example.com/document";
await client.getChunksByUrl({ accessToken, url });

// Document Name Search : retrieve all chunks of a document identified by its name
const documentName = "AI Research Paper";
await client.queryChunksByDocumentName({ accessToken, documentName });
```

## Multi-User Client

The `MultiUserClient` class helps manage multiple users' authentication and access to the Redactive search service.

```typescript
import { MultiUserClient } from "@redactive/redactive";

const multiUserClient = MultiUserClient(
  "REDACTIVE-API-KEY",
  "https://example.com/callback/",
  readUserData,
  multiUserClient
);

// Present `connection_url` in browser for user to interact with:
const userId = "myUserId";
const connectionUrl = await multiUserClient.getBeginConnectionUrl(userId, "confluence");

// On user return from OAuth connection flow:
let [signInCode, state] = ["", ""]; // from URL query parameters
const isConnectionSuccessful = await multiUserClient.handleConnectionCallback(userId, signInCode, state);

// User can now use Redactive search service via `MultiUserClient`'s other methods:
const semanticQuery = "Tell me about the missing research vessel, the Borealis";
const chunks = await multiUserClient.queryChunks({ userId, semanticQuery });
```

## Development

The Node SDK code can be found the`sdks/node` directory in Redactive Github Repository.

In order to comply with the repository style guide, we recommend running the following tools.

To format your code, run:

```sh
pnpm format:fix
```

To lint your code, run:

```sh
pnpm lint:fix
```

To test changes, run:

```sh
pnpm test
```

To build Python SDK, run:

```sh
pnpm build
```

To install local version, run:

```sh
npm install ./sdks/node
```

## Contribution Guide

Please check [here](https://github.com/redactive-ai/redactive?tab=readme-ov-file#contribution-guide)
