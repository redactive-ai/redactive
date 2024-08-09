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

- Node v22+

## Usage

The library has following components.

- **AuthClient** - provides functionality to interact with data sources
- **SearchClient** - provides functionality to search chunks with Redactive search service in gRPC

### AuthClient

AuthClient needs to be configured with your account's API key which is
available in the Apps page at [Redactive Dashboard](https://dashboard.redactive.ai/).

```javascript
import { AuthClient } from "@redactive/redactive";

// Establish an connection to data source
// Possible data sources: confluence, google-drive, jira, zendesk, slack, sharepoint
const redirectUri = "https://url-debugger.vercel.app";
const provider = "confluence";
const signInUrl = await client.beginConnection(provider, redirectUri);

// Navigate User to signInUrl
// User will receive an oauth2 auth code after consenting the app's data source access permissions.
// Use this code to exchange Redactive access_token with Redactive API
const response = await client.exchangeTokens("OAUTH2-AUTH-CODE");
```

### SearchClient

With the Redactive access_token, User can search documents with Redactive Search service.

```javascript
import { SearchClient } from "@redactive/redactive";

const client = new SearchClient();
await client.queryChunks("REDACTIVE-ACCESS-TOKEN", "Tell me about AI");
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
