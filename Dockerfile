FROM ubuntu:22.04

# Constants
ARG BUILDER_NAME="multiversx/sdk-rust-contract-builder:v4.1.3"
ARG VERSION_RUST="nightly-2022-10-16"
ARG VERSION_BINARYEN="105-1"

# Install dependencies (including binaryen)
RUN apt-get update && apt-get install -y \
    wget \ 
    build-essential \
    python3.11 python-is-python3 python3-pip \
    binaryen=${VERSION_BINARYEN}

RUN pip3 install toml==0.10.2 semver==3.0.0-dev.4

# Install rust
RUN wget -O rustup.sh https://sh.rustup.rs && \
    chmod +x rustup.sh && \
    CARGO_HOME=/rust RUSTUP_HOME=/rust ./rustup.sh --verbose --default-toolchain ${VERSION_RUST} --profile minimal --target wasm32-unknown-unknown -y && \
    rm rustup.sh && \
    chmod -R 777 /rust && \
    rm -rf /rust/registry


# Install sc-tool
RUN apt-get update && apt-get install -y git && \
    git clone https://github.com/multiversx/mx-sdk-rs.git --branch=meta-local-deps --single-branch --depth=1 && \
    chmod -R 777 /mx-sdk-rs && \
    cd /mx-sdk-rs/framework/meta && \
    PATH="/rust/bin:${PATH}" CARGO_HOME=/rust RUSTUP_HOME=/rust cargo install --path . && \
    rm -rf /rust/registry && \
    apt-get remove -y git

COPY "multiversx_sdk_rust_contract_builder" "/multiversx_sdk_rust_contract_builder"

ENV PATH="/rust/bin:${PATH}"
ENV CARGO_HOME="/rust"
ENV RUSTUP_HOME="/rust"
ENV PYTHONPATH=/
ENV BUILD_METADATA_BUILDER_NAME=${BUILDER_NAME}
ENV BUILD_METADATA_VERSION_RUST=${VERSION_RUST}
ENV BUILD_METADATA_VERSION_BINARYEN=${VERSION_BINARYEN}

# Additional arguments (must be provided at "docker run"):
# --project or --packaged-src
# --no-wasm-opt (optional)
# --build-root (optional)
ENTRYPOINT ["python", "/multiversx_sdk_rust_contract_builder/main.py", \
    "--output", "/output", \
    "--cargo-target-dir", "/rust/cargo-target-dir"]

LABEL frozen="yes"
LABEL rust=${VERSION_RUST}
LABEL wasm-opt-binaryen=${VERSION_BINARYEN}
LABEL wabt=${VERSION_WABT}
