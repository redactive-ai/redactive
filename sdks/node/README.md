# Redactive Node SDK

The Redactive Node SDK provides a robust and intuitive interface for interacting with the Redactive platform, enabling developers to seamlessly integrate powerful data redaction and anonymization capabilities into their Node applications.

## Installation

In order to use the package to integrate with Redactive.ai, run:

```sh
npm install @redactive/redactive
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

The AuthClient can be used to present users with the data providers' OAuth consent
pages:

```javascript
import { AuthClient } from "@redactive/redactive";

// Construct AuthClient using your Redactive API key
const client = new AuthClient("YOUR-API-KEY-HERE");

// Establish an connection to data source
// Possible data sources: confluence, sharepoint
const redirectUri = "YOUR-REDIRECT-URI";
const provider = "confluence";
const signInUrl = await client.beginConnection({ provider, redirectUri });

// Now redirect your user to signInUrl
```

The user will be redirected back to your app's configured redirect uri after they have completed the steps on
the data provider's OAuth consent page. There will be a signin code present in the `code` parameter of the query string e.g.
`https://your-redirect-page.com?code=abcde12345`.

This code may be exchanged for a user access token (which the user may use to issue queries against their data):

```javascript
// Exchange signin code for a Redactive ID token
const response = await client.exchangeTokens({ code: "SIGNIN-CODE" });
const accessToken = response.idToken;
```

Once a user has completed the OAuth flow, the data source should show up in their connected data sources:

```javascript
(await client.listConnections({ accessToken }).connections) === ["confluence"]; // ✅
```

Use the `list_connections` method to keep your user's connection status up to date, and provide mechanisms to re-connect data sources.

### SearchClient

With the Redactive `access_token`, you can perform two types of search

#### Query-based Search

Retrieve relevant chunks of information that are related to a user query.

```javascript
import { SearchClient } from "@redactive/redactive";

const client = new SearchClient();
const accessToken = "REDACTIVE-ACCESS-TOKEN";

// Query-based Search: retrieve text extracts (chunks) from various documents pertaining to the user query
const query = "Tell me about AI";
await client.searchChunks({ accessToken, query });
```

**Filters** may be applied to query-based search operations. At present, the following fields may be provided as filter predicates:

```protobuf
message Filters {
    // Scope of the query. This may either be the name of a provider, or a subspace of documents.
    // Subspaces take the form of <provider>://<tenancy>/<path>
    // e.g. for Confluence: 'confluence://redactiveai.atlassian.net/Engineering/Engineering Onboarding Guide'
    // for Sharepoint: 'sharepoint://redactiveai.sharepoint.com/Shared Documents/Engineering/Onboarding Guide.pdf'
    repeated string scope = 1;
    // Timespan of response chunk's creation
    optional TimeSpan created = 2;
    // Timespan of response chunk's last modification
    optional TimeSpan modified = 3;
    // List of user emails associated with response chunk
    repeated string user_emails = 4;
    // Include content from documents in trash
    optional bool include_content_in_trash = 5;
}
```

The query will only return results which match _ALL_ filter predicates i.e. if multiple fields are populated in the filter object,
the resulting filter is the logical 'AND' of all the fields. If a data source provider does not support a filter-type, then no
results from that provider are returned.

Filters may be populated and provided to a query in the following way for the NodeJS SDK:

```javascript
import { Filters } from "@redactive/redactive";

// Query chunks from Confluence only, that are from documents created before last week, modified since last week,
// and that are from documents associated with a user's email. Include chunks from trashed documents.
const lastWeek = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
const filters: Filters = {
  scope: ["confluence"],
  created: {
    before: lastWeek
  },
  modified: {
    after: lastWeek
  },
  userEmails: ["myEmail@example.com"],
  includeContentInTrash: true
};
await client.searchChunks({ accessToken, semanticQuery, filters });

```

#### Document Fetch

Obtain all the chunks from a specific document by specifying a unique reference (i.e. a URL).

```javascript
import { SearchClient } from "@redactive/redactive";

const client = new SearchClient();
const accessToken = "REDACTIVE-ACCESS-TOKEN";

// URL-based Search: retrieve all chunks of the document at that URL
const url = "https://example.com/document";
await client.getDocument({ accessToken, url });
```

### Multi-User Client

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
const query = "Tell me about the missing research vessel, the Borealis";
const chunks = await multiUserClient.searchChunks({ userId, query });
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
