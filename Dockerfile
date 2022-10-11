FROM ubuntu:22.04

# Constants
ARG VERSION_RUST="nightly-2022-08-23"
ARG VERSION_BINARYEN="105-1"
ARG VERSION_WABT="1.0.27-1"

RUN apt-get update && apt-get install wget -y
RUN apt-get update && apt-get install python3.10 python-is-python3 -y
RUN apt-get update && apt-get install build-essential -y

# Install rust
RUN wget -O rustup.sh https://sh.rustup.rs && \
    chmod +x rustup.sh && \
    CARGO_HOME=/rust RUSTUP_HOME=/rust ./rustup.sh --verbose --default-toolchain ${VERSION_RUST} --profile minimal --target wasm32-unknown-unknown -y && \
    rm rustup.sh

# Install wasm-opt
RUN apt-get update && apt-get install binaryen=${VERSION_BINARYEN}

# Install wabt
RUN apt-get update && apt-get install wabt=${VERSION_WABT}

COPY "./build_within_docker.py" "/build.py"

ENV PATH="/rust/bin:${PATH}"
ENV CARGO_HOME="/rust"
ENV RUSTUP_HOME="/rust"

# Additional arguments (must be provided at "docker run"):
# --output-owner-id
# --output-group-id
# --no-wasm-opt (optional)
ENTRYPOINT ["python", "./build.py", \
    "--project", "/project", \
    "--output", "/output", \
    "--cargo-target-dir", "/cargo-target-dir"]

LABEL frozen="yes"
LABEL rust=${VERSION_RUST}
LABEL wasm-opt-binaryen=${VERSION_BINARYEN}
LABEL wabt=${VERSION_WABT}
