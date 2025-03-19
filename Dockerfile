FROM ubuntu:22.04

# Constants
ARG VERSION_RUST="1.85.0"
ARG VERSION_SC_META="0.57.0"
ARG TARGETPLATFORM

# Install system dependencies
RUN apt-get update --fix-missing && apt-get install -y \
    wget \
    build-essential \
    git \
    python3.11 python-is-python3 python3-pip \
    pkg-config \
    libssl-dev

# Install Python dependencies
RUN pip3 install toml==0.10.2 semver==3.0.0-dev.4

# Install rust
RUN wget -O rustup.sh https://sh.rustup.rs && \
    chmod +x rustup.sh && \
    CARGO_HOME=/rust RUSTUP_HOME=/rust ./rustup.sh --verbose --default-toolchain ${VERSION_RUST} --profile minimal --target wasm32-unknown-unknown -y && \
    rm rustup.sh && \
    chmod -R 777 /rust && \
    rm -rf /rust/registry

# Install sc-meta tool
RUN PATH="/rust/bin:${PATH}" CARGO_HOME=/rust RUSTUP_HOME=/rust cargo install multiversx-sc-meta --version ${VERSION_SC_META} --locked && \
    rm -rf /rust/registry

COPY "multiversx_sdk_rust_contract_builder" "/multiversx_sdk_rust_contract_builder"

ENV PATH="/rust/bin:${PATH}"
ENV CARGO_HOME="/rust"
ENV RUSTUP_HOME="/rust"
ENV PYTHONPATH=/
ENV BUILD_METADATA_VERSION_RUST=${VERSION_RUST}
ENV BUILD_METADATA_VERSION_SC_META=${VERSION_SC_META}
ENV BUILD_METADATA_TARGETPLATFORM=${TARGETPLATFORM}

# Additional arguments (must be provided at "docker run"):
# --project or --packaged-src
# --no-wasm-opt (optional)
# --build-root (optional)
ENTRYPOINT ["python", "/multiversx_sdk_rust_contract_builder/main.py", \
    "--output", "/output", \
    "--cargo-target-dir", "/rust/cargo-target-dir"]

LABEL frozen="yes"
LABEL rust=${VERSION_RUST}
LABEL sc_meta=${VERSION_SC_META}
