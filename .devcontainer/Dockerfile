ARG VARIANT="3.12-bookworm"
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    protobuf-compiler>=3.21.12 \
    libprotobuf-dev>=3.21.12 \
    && rm -rf /var/lib/apt/lists/*

# Install/upgrade pip, build, twine
RUN python -m pip install --upgrade \
    pip \
    hatch \
    grpcio-tools \
    betterproto[compiler]==2.0.0b6 \
    pre-commit

RUN curl -fsSL https://deb.nodesource.com/setup_20.x -o nodesource_setup.sh \
    && bash nodesource_setup.sh 

RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    && rm -rf /var/lib/apt/lists/*

RUN npm install --no-fund -g \
    prettier \
    ts-proto@2.0.2 \
    pnpm
