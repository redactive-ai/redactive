# Redactive

The Redactive Application, Docs &amp; Samples

## Directory Structure

`├──`[`.devcontainer`](.devcontainer/) — Docker dev container configuration<br>
`├──`[`.github`](.github/) — GitHub configuration including CI/CD workflows<br>
`├──`[`.vscode`](.vscode/) — VS Code configuration<br>
`├──`[`protos`](protos/) — Redactive gRpc protocol<br>
`├──`[`sdks`](sdks/python/) — Redactive SDKs<br>
`├──`[`.pre-commit-config.yaml`](.pre-commit-config.yaml) — Pre-commit hooks<br>
`└──`[`.prettierrc.yaml`](.prettierrc.yaml) — Prettier configuration<br>

## Building the Python SDK

`cd sdks/python`

`python -m pip install --upgrade build`

`python -m build`

