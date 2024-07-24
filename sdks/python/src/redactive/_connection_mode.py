import os
from enum import StrEnum


class ConnectionMode(StrEnum):
    Internet = "internet"
    AWSPrivateLink = "awsprivatelink"
    AzurePrivateLink = "azureprivatelink"
    GCPPrivateServiceConnect = "gcpprivateserviceconnect"


def _get_environment_connection_mode() -> ConnectionMode:
    connection_mode_str = os.environ.get("REDACTIVE_CONNECTION_MODE", ConnectionMode.Internet.value).lower()
    try:
        return ConnectionMode(connection_mode_str)
    except ValueError as e:
        msg = f"Invalid env var REDACTIVE_CONNECTION_MODE set to '{connection_mode_str}'"
        raise ValueError(msg) from e


_endpoints = {
    ConnectionMode.Internet: {"http": "https://api.redactive.ai", "grpc": ("grpc.redactive.ai", 443)},
    ConnectionMode.AWSPrivateLink: {
        "http": "https://awsprivatelink.redactive.app",
        "grpc": ("awsprivatelink.redactive.app", 50443),
    },
}


def get_default_http_endpoint() -> str:
    cm = _get_environment_connection_mode()
    if cm not in _endpoints:
        msg = f"{cm} is coming soon and not yet supported as a connection mode"
        raise ValueError(msg)
    return _endpoints[cm]["http"]


def get_default_grpc_host_and_port() -> tuple[str, int]:
    cm = _get_environment_connection_mode()
    if cm not in _endpoints:
        msg = f"{cm} is coming soon and not yet supported as a connection mode"
        raise ValueError(msg)
    return _endpoints[cm]["grpc"]
