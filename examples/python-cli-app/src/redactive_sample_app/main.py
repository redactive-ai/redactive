import datetime

import asyncclick as click
from typing import Optional

from redactive.search_client import SearchClient
from redactive.auth_client import AuthClient

@click.group()
def cli():
    pass


@cli.command()
@click.option("--count", default=1, help="Number of chunks to return.")
@click.option("--credential", prompt="Your API key", help="Your application's API key.")
@click.option(
    "--host", prompt="Host", help="The host to connect to.", default="grpc.redactive.ai"
)
@click.option("--port", prompt="Port", help="The port to connect to.", default=443)
@click.option("--datasource", help="The datasource to use", default=None)
async def query(count: int, credential: str, host: str, datasource: Optional[str] = None, port=443):
    """Simple program that lets you search queries based on semantic meaning."""

    # Create a SearchClient instance with the provided host and port
    client = SearchClient(host=host, port=port)

    filter_dict = dict()

    if datasource:
        filter_dict.update(dict(scope=[datasource]))

    while True:
        semantic_query = input("Enter a query: ")
        if not semantic_query:
            break
        chunks = await client.query_chunks(access_token=credential, semantic_query=semantic_query, count=count, query_filter=filter_dict)
        for chunk in chunks:
            print(chunk.chunk_body)
            print("METADATA", chunk.document_metadata)


@cli.command()
@click.option("--app-key", prompt="Your App key", help="Your application's API key.")
@click.option(
    "--datasource",
    prompt="Your datasource",
    help="Your datasource.",
    type=click.Choice(["confluence", "sharepoint", "jira", "slack", "zendesk", "google-drive"]),
)
@click.option("--redirect-uri", prompt="Redirect URI", help="Your redirect URI.", default="https://url-debugger.vercel.app/")
@click.option(
    "--host", prompt="Host", help="The host to connect to.", default="https://api.redactive.ai"
)
@click.option("--endpoint", help="The endpoint to connect to.", default=None)
@click.option("--code-param-alias", help="The code param alias.", default=None)
async def setup_datasource(app_key: str, datasource: str, redirect_uri: str, host: str, endpoint: Optional[str] = None, code_param_alias: Optional[str] = None):
    """
    Setup a datasource with the provided API key and datasource type. This will allow the user to query the datasource.
    """

    # Create an AuthClient instance with the provided API key and host
    client = AuthClient(api_key=app_key, base_url=host)

    # Begin the connection to the datasource
    sign_in_url = await client.begin_connection(provider=datasource, redirect_uri=redirect_uri, endpoint=endpoint, code_param_alias=code_param_alias)

    print(
        f"Go to the following URL to authenticate your {datasource} datasource: {sign_in_url}"
    )
    print("")
    code = input("Enter the code parameter found in the callback URL: ")
    print("")

    # Exchange the code for an access token
    response = await client.exchange_tokens(code=code)

    # Print the access token, refresh token, and expiration time
    print(f"Your datasource {datasource} has been setup with the following tokens:")
    print(f"Access Token: {response.idToken}\n")
    print(f"Refresh Token: {response.refreshToken}\n")
    expires_at = datetime.datetime.now() + datetime.timedelta(
        seconds=int(response.expiresIn)
    )
    print(f"Expires at: {expires_at.strftime('%Y-%m-%d %H:%M:%S')}")


@cli.command()
@click.option("--app-key", prompt="Your App key", help="Your application's API key.")
@click.option("--refresh-token", prompt="Your refresh token", help="Your refresh token.")
@click.option(
    "--host", prompt="Host", help="The host to connect to.", default="https://api.redactive.ai"
)
async def refresh_token(app_key: str, refresh_token: str, host: str):
    """
    Refresh the access token with the provided API key and refresh token.
    """

    # Create an AuthClient instance with the provided API key and host
    client = AuthClient(api_key=app_key, base_url=host)

    # Exchange the refresh token for a new access token
    response = await client.exchange_tokens(refresh_token=refresh_token)

    # Print the new access token, refresh token, and expiration time
    print(f"Your new access token is: {response.idToken}")
    print(f"Your new refresh token is: {response.refreshToken}")
    expires_at = datetime.datetime.now() + datetime.timedelta(
        seconds=int(response.expiresIn)
    )
    print(f"Expires at: {expires_at.strftime('%Y-%m-%d %H:%M:%S')}")