FROM ubuntu:22.04

# Constants
ARG VERSION_RUST="nightly-2022-10-16"
ARG VERSION_BINARYEN="105-1"
ARG VERSION_WABT="1.0.27-1"
ARG CONTEXT="multiversx/sdk-rust-contract-builder:v4.1.2"

# Install dependencies (including binaryen and wabt)
RUN apt-get update && apt-get install -y \
    wget \ 
    build-essential \
    python3.11 python-is-python3 python3-pip \
    binaryen=${VERSION_BINARYEN} \
    wabt=${VERSION_WABT}

RUN pip3 install tomlkit==0.11.6 semver==2.13.0

# Install rust
RUN wget -O rustup.sh https://sh.rustup.rs && \
    chmod +x rustup.sh && \
    CARGO_HOME=/rust RUSTUP_HOME=/rust ./rustup.sh --verbose --default-toolchain ${VERSION_RUST} --profile minimal --target wasm32-unknown-unknown -y && \
    rm rustup.sh && \
    chmod -R 777 /rust

COPY "multiversx_sdk_rust_contract_builder" "/multiversx_sdk_rust_contract_builder"

ENV PATH="/rust/bin:${PATH}"
ENV CARGO_HOME="/rust"
ENV RUSTUP_HOME="/rust"
ENV CONTEXT=${CONTEXT}
ENV PYTHONPATH=/

# Additional arguments (must be provided at "docker run"):
# --project or --packaged-src
# --no-wasm-opt (optional)
ENTRYPOINT ["python", "/multiversx_sdk_rust_contract_builder/main.py", \
    "--output", "/output", \
    "--cargo-target-dir", "/rust/cargo-target-dir"]

LABEL frozen="yes"
LABEL rust=${VERSION_RUST}
LABEL wasm-opt-binaryen=${VERSION_BINARYEN}
LABEL wabt=${VERSION_WABT}
