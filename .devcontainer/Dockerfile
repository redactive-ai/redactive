ARG VARIANT="3.12-bookworm"
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    protobuf-compiler \
    libprotobuf-dev \
    && rm -rf /var/lib/apt/lists/*

# Install/upgrade pip, build, twine
RUN python -m pip install --upgrade \
    pip \
    hatch \
    grpcio-tools \
    betterproto[compiler]==2.0.0b6 \
    pre-commit

RUN curl -fsSL https://deb.nodesource.com/setup_22.x -o nodesource_setup.sh \
    && bash nodesource_setup.sh 

RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    && rm -rf /var/lib/apt/lists/*

RUN npm install --no-fund -g \
    prettier
