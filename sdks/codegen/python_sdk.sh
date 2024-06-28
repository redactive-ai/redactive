#!/bin/sh

# Generate Python SDK
# Python SDK Path
PYTHON_SDK_OUTPUT_PATH=sdks/python

# Generate Python SDK code with protobuf files
python -m grpc_tools.protoc \
    --proto_path=protos \
    --python_betterproto_out=$PYTHON_SDK_OUTPUT_PATH/src \
    search.proto

# Removed unwanted __init__.py
rm -f $PYTHON_SDK_OUTPUT_PATH/src/__init__.py

# Lints generated code
ruff check \
    --config=$PYTHON_SDK_OUTPUT_PATH/pyproject.toml \
    --fix \
    $PYTHON_SDK_OUTPUT_PATH/src/redactive/grpc

# Formats generated code
ruff format \
    --config=$PYTHON_SDK_OUTPUT_PATH/pyproject.toml \
    $PYTHON_SDK_OUTPUT_PATH/src/redactive/grpc