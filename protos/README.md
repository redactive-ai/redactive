# Redactive gRpc Protocols

## Directory Structure

`├──`[`chunks.proto`](chunks.proto) — Chunk structure definition<br>
`└──`[`search.proto`](search.proto) — Search service protocol<br>

## Generate Code from Protobuf

### Python

- Install required packages `pip install grpcio-tools betterproto[compiler]==2.0.0b6`
- Here is an example to generate search service

```bash
python3 -m grpc_tools.protoc -I protos --python_betterproto_out={{OUTPUT_PATH}} search.proto
```
