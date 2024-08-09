#!/bin/sh

# Generate Node SDK
NODE_MODULES_DIR=$(npm root -g)
NODE_SDK_DIR=sdks/node
NODE_SDK_OUTPUT_DIR=sdks/node/src/grpc
mkdir -p ${NODE_SDK_OUTPUT_DIR}
PROTO_DIR=protos

protoc \
   -I protos \
   --experimental_allow_proto3_optional=1 \
   --plugin=${NODE_MODULES_DIR}/ts-proto/protoc-gen-ts_proto \
   --ts_proto_opt=outputServices=grpc-js \
   --ts_proto_out=${NODE_SDK_OUTPUT_DIR} \
   search.proto
