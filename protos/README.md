# Redactive gRpc Protocols

## Directory Structure

`├──`[`chunks.proto`](chunks.proto) — Chunk structure definition<br>
`└──`[`search.proto`](search.proto) — Search service protocol<br>

## Generate Code from Protobuf

### Python

- Install required packages `pip install grpcio-tools betterproto[compiler]==2.0.0b6`
- Here is an example to generate search service

```bash
OUTPUT_PATH=
python3 -m grpc_tools.protoc \
  --proto_path=protos \
  --python_betterproto_out=${OUTPUT_PATH} \
   search.proto
```

### Node

- Install protobuf compiler https://grpc.io/docs/protoc-installation
- Install libprotobuf-dev for Linux
- Install required packages `npm install -g ts-proto`
- Here is an example to generate search service

```bash
NODE_MODULES_DIR=$(npm root -g)
OUTPUT_PATH=
protoc \
  -I protos \
  --experimental_allow_proto3_optional=1 \
  --plugin=${NODE_MODULES_DIR}/ts-proto/protoc-gen-ts_proto \
   --ts_proto_opt=outputServices=grpc-js \
   --ts_proto_out=${OUTPUT_PATH} \
 search.proto
```

ps. Use Redactive devcontainer for best outcome.
