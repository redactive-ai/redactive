#!/bin/sh

# Python SDK Path
SDK_OUTPUT_PATH=sdks/python

# Generate Python SDK code with protobuf files
python -m grpc_tools.protoc \
    --proto_path=protos \
    --python_betterproto_out=$SDK_OUTPUT_PATH/src \
    search.proto

# Removed unwanted __init__.py
rm -f $SDK_OUTPUT_PATH/src/__init__.py

# Lints generated code
ruff check \
    --config=$SDK_OUTPUT_PATH/pyproject.toml \
    --fix \
    $SDK_OUTPUT_PATH/src/redactive/grpc

# Formats generated code
ruff format \
    --config=$SDK_OUTPUT_PATH/pyproject.toml \
    $SDK_OUTPUT_PATH/src/redactive/grpc