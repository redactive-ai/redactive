#!/bin/sh

# Generate Python SDK
# Python SDK Path
SCRIPT_PATH=$(dirname "$(realpath $0)")
PYTHON_SDK_OUTPUT_PATH=$SCRIPT_PATH/../python

# Generate Python SDK code with protobuf files
python -m grpc_tools.protoc \
    --proto_path=protos \
    --python_betterproto_out=$PYTHON_SDK_OUTPUT_PATH/src \
    search.proto

# Removed unwanted __init__.py
rm -f $PYTHON_SDK_OUTPUT_PATH/src/__init__.py

