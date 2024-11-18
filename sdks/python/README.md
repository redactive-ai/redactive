# Redactive Python SDK

The Redactive Python SDK provides a robust and intuitive interface for interacting with the Redactive platform, enabling developers to seamlessly integrate powerful data redaction and anonymization capabilities into their Python applications.

## Installation

In order to use the package to integrate with Redactive.ai, run:

```sh
pip install --upgrade redactive
```

There is no need to clone this repository.

If you would like to modify this package, clone the repo and install from source:

```sh
python -m pip install .
```

### Requirements

- Python 3.11+

## Usage

The library has the following components:

- **AuthClient** - provides functionality to interact with data sources
- **SearchClient** - provides functionality to search chunks with Redactive search service
- **MultiUserClient** - provides functionality manage multi-user search with Redactive search service
- **RerankingSearchClient** [Experimental] - retrieves extra results, then re-ranks them using a more precise ranking function, returning the top_k results

### AuthClient

AuthClient needs to be configured with your account's API key which is
available in the Apps page at [Redactive Dashboard](https://dashboard.redactive.ai/).

```python
from redactive.auth_client import AuthClient

client = AuthClient(api_key="API-KEY")

# Establish an connection to data source
# Possible data sources: confluence, google-drive, jira, zendesk, slack, sharepoint
redirect_uri = "https://url-debugger.vercel.app"
sign_in_url = await client.begin_connection(
    provider="confluence", redirect_uri=redirect_uri
)

# Navigate User to sign_in_url
# User will receive an oauth2 auth code after consenting the app's data source access permissions.
# Use this code to exchange Redactive access_token with Redactive API
response = await client.exchange_tokens(code="OAUTH2-TOKEN")
```

### SearchClient

With a Redactive access_token, you can perform two types of search

#### Query-based Search

Retrieve relevant chunks of information that are related to a user query.

```python
from redactive.search_client import SearchClient

client = SearchClient()

# Semantic Search: retrieve text extracts (chunks) from various documents pertaining to the user query
client.search_chunks(
    access_token="REDACTIVE-USER-ACCESS-TOKEN",
    query="Tell me about AI"
)
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

Filters may be populated and provided to a query in the following way for the Python SDK:

```python
from datetime import datetime, timedelta
from redactive.search_client import SearchClient
from redactive.grpc.v1 import Filters

client = SearchClient()

# Query chunks from Confluence only, that are from documents created before last week, modified since last week,
# and that are from documents associated with a user's email. Include chunks from trashed documents.
last_week = datetime.now() - timedelta(weeks=1)
filters = Filters().from_dict({
  "scope": ["confluence"],
  "created": {
    "before": last_week,
  },
  "modified": {
    "after": last_week,
  },
  "userEmails": ["myEmail@example.com"],
  "includeContentInTrash": True,
})
client.query_chunks(
    access_token="REDACTIVE-USER-ACCESS-TOKEN",
    semantic_query="Tell me about AI",
    filters=filters
)
```


#### Document Fetch

Obtain all the chunks from a specific document by specifying  a unique reference (i.e. a URL).

```python
# URL-based Search: retrieve all chunks of the document at that URL
client.get_document(
    access_token="REDACTIVE-USER-ACCESS-TOKEN",
    ref="https://example.com/document"
)
```

### Multi-User Client

The `MultiUserClient` class helps manage multiple users' authentication and access to the Redactive search service.

```python
from redactive.multi_user_client import MultiUserClient

multi_user_client = MultiUserClient(
    api_key="REDACTIVE-API-KEY",
    callback_uri="https://example.com/callback/",
    read_user_data=...,
    write_user_data=...,
)

# Present `connection_url` in browser for user to interact with:
user_id = ...
connection_url = await multi_user_client.get_begin_connection_url(user_id=user_id, provider="confluence")

# On user return from OAuth connection flow:
sign_in_code, state = ..., ...  # from URL query parameters
is_connection_successful = await multi_user_client.handle_connection_callback(
    user_id=user_id,
    sign_in_code=sign_in_code,
    state=state
)

# User can now use Redactive search service via `MultiUserClient`'s other methods:
query = "Tell me about the missing research vessel, the Borealis"
chunks = await multi_user_client.search_chunks(user_id=user_id, query=query)
```

## Development

The Python SDK code can be found the`sdks/python` directory in Redactive Github Repository.

In order to comply with the repository style guide, we recommend running the following tools.

To format your code, run:

```sh
hatch fmt
```

To check type, run:

```sh
hatch run types:check
```

To test changes, run:

```sh
hatch test
```

To build Python SDK, run:

```sh
hatch build
```

To install local version, run:

```sh
python -m pip install -e .
```

## Contribution Guide

Please check [here](https://github.com/redactive-ai/redactive?tab=readme-ov-file#contribution-guide)
