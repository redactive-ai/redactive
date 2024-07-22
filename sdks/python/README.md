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

The library has following components.

- **AuthClient** - provides functionality to interact with data sources
- **SearchClient** - provides functionality to search chunks with Redactive search service in gRPC
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

With the Redactive access_token, User can search documents with Redactive Search service.

```python
from redactive.search_client import SearchClient

client = SearchClient()

client.query_chunks(
    access_token="REDACITVE-USER-ACCESS-TOKEN",
    semantic_query="Tell me about AI"
)
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
