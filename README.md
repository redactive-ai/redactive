# Redactive

The Redactive Application, Docs & Samples

## Directory Structure

`├──`[`.devcontainer`](.devcontainer/) — Docker dev container configuration<br>
`├──`[`.github`](.github/) — GitHub configuration including CI/CD workflows<br>
`├──`[`.vscode`](.vscode/) — VS Code configuration<br>
`├──`[`protos`](protos/) — Redactive gRpc protocol<br>
`├──`[`sdks`](sdks) — Redactive SDKs<br>
`├──`[`.pre-commit-config.yaml`](.pre-commit-config.yaml) — Pre-commit hooks<br>
`└──`[`.prettierrc.yaml`](.prettierrc.yaml) — Prettier configuration<br>

## Contribution Guide

This repository is configured to run formatting, testing, linting with pre-commit hooks. Read [`.pre-commit-config.yaml`](.pre-commit-config.yaml) for more details.

### PR Creation Flow

1. **Fork the Repository**: Click the "Fork" button on the repository's GitHub page.
2. **Clone Your Fork**: Clone the forked repository to your local machine.
3. **Create a New Branch**: Create and switch to a new branch for your changes.
4. **Make Changes**: Make your changes, then stage and commit them.
5. **Push the Changes**: Push your branch to your forked repository.
6. **Create a Pull Request**: On GitHub, open a pull request from your branch to the Redactive repository's main branch.
7. **Respond to Feedback**: Make any requested changes and push them to your branch.

### PR Review Flow

- Ensure quality checks pass.
- Ensure the build process passes.
- Reviewer reviews and responds to code changes.
- Reviewer merges approved code changes.
