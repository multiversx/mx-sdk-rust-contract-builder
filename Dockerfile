FROM ubuntu:22.04

# Constants
ARG VERSION_RUST="nightly-2022-10-16"
ARG VERSION_BINARYEN="105-1"
ARG VERSION_WABT="1.0.27-1"

# Install dependencies (including binaryen and wabt)
RUN apt-get update && apt-get install -y \
    wget \ 
    build-essential \
    python3.10 python-is-python3 \
    binaryen=${VERSION_BINARYEN} \
    wabt=${VERSION_WABT}

# Install rust
RUN wget -O rustup.sh https://sh.rustup.rs && \
    chmod +x rustup.sh && \
    CARGO_HOME=/rust RUSTUP_HOME=/rust ./rustup.sh --verbose --default-toolchain ${VERSION_RUST} --profile minimal --target wasm32-unknown-unknown -y && \
    rm rustup.sh && \
    chmod -R 777 /rust

COPY "build_contract_rust" "/build_contract_rust"

ENV PATH="/rust/bin:${PATH}"
ENV CARGO_HOME="/rust"
ENV RUSTUP_HOME="/rust"
ENV PYTHONPATH=/

# Additional arguments (must be provided at "docker run"):
# --project or --packaged-src
# --no-wasm-opt (optional)
ENTRYPOINT ["python", "/build_contract_rust/main.py", \
    "--output", "/output", \
    "--cargo-target-dir", "/rust/cargo-target-dir"]

LABEL frozen="yes"
LABEL rust=${VERSION_RUST}
LABEL wasm-opt-binaryen=${VERSION_BINARYEN}
LABEL wabt=${VERSION_WABT}
