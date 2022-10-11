FROM ubuntu:20.04

# Constants
ARG VERSION_RUST="nightly-2022-08-23"
ARG VERSION_BINARYEN="version_105"
ARG VERSION_WABT="1.0.27"

RUN apt-get update && apt-get install wget -y
RUN apt-get update && apt-get install python3.8 python-is-python3 -y
RUN apt-get update && apt-get install build-essential -y

# Install rust
RUN wget -O rustup.sh https://sh.rustup.rs && \
    chmod +x rustup.sh && \
    CARGO_HOME=/rust RUSTUP_HOME=/rust ./rustup.sh --verbose --default-toolchain ${VERSION_RUST} --profile minimal --target wasm32-unknown-unknown -y && \
    rm rustup.sh

# Install wasm-opt
RUN wget -O binaryen.tar.gz https://github.com/WebAssembly/binaryen/releases/download/${VERSION_BINARYEN}/binaryen-${VERSION_BINARYEN}-x86_64-linux.tar.gz && \
    tar -xf binaryen.tar.gz && mv binaryen-${VERSION_BINARYEN}/bin/wasm-opt /usr/bin && \
    rm binaryen.tar.gz && \
    rm -rf binaryen-${VERSION_BINARYEN}

# Install wabt
RUN wget -O wabt.tar.gz https://github.com/WebAssembly/wabt/releases/download/${VERSION_WABT}/wabt-${VERSION_WABT}-ubuntu.tar.gz && \
    tar -xf wabt.tar.gz && mv wabt-${VERSION_WABT}/bin/wasm2wat /usr/bin && mv wabt-${VERSION_WABT}/bin/wasm-objdump /usr/bin && \
    rm wabt.tar.gz && \
    rm -rf wabt-${VERSION_WABT}


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

