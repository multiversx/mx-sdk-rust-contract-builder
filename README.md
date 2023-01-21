# mx-sdk-rust-contract-builder

Docker image (and wrappers) for reproducible contract builds (Rust). See [docs.multiversx.com](https://docs.multiversx.com/developers/reproducible-contract-builds/).

## Build the Docker image

```
docker buildx build --no-cache . -t sdk-rust-contract-builder:next -f ./Dockerfile
```

## Build contract using the wrapper

Without providing `cargo-target-dir`:

```
python3 ./build_with_docker.py --image=sdk-rust-contract-builder:next \
    --project=~/contracts/reproducible-contract-build-example \
    --output=~/contracts/output-from-docker
```

With providing `cargo-target-dir`:

```
python3 ./build_with_docker.py --image=sdk-rust-contract-builder:next \
    --project=~/contracts/reproducible-contract-build-example \
    --output=~/contracts/output-from-docker \
    --cargo-target-dir=~/cargo-target-dir-docker
```

Building from a packaged source code:

```
python3 ./build_with_docker.py --image=sdk-rust-contract-builder:next \
    --packaged-src=~/contracts/example-0.0.0.source.json \
    --output=~/contracts/output-from-docker
```

## Build contract using the Docker inner script

This is useful for useful for testing, debugging and reviewing the script.

```
export PROJECT=${HOME}/contracts/reproducible-contract-build-example
export OUTPUT=${HOME}/contracts/output
export CARGO_TARGET_DIR=${HOME}/cargo-target-dir
export PATH=${HOME}/multiversx-sdk/vendor-rust/bin:${HOME}/multiversx-sdk/wabt/latest/bin:${PATH}
export RUSTUP_HOME=${HOME}/multiversx-sdk/vendor-rust
export CARGO_HOME=${HOME}/multiversx-sdk/vendor-rust
```

Build a project:

```
python3 ./build_within_docker.py --project=${PROJECT} --output=${OUTPUT} \
    --cargo-target-dir=${CARGO_TARGET_DIR}
```

## Run tests

```
export PATH=${HOME}/multiversx-sdk/vendor-rust/bin:${HOME}/multiversx-sdk/wabt/latest/bin:${PATH}
export RUSTUP_HOME=${HOME}/multiversx-sdk/vendor-rust
export CARGO_HOME=${HOME}/multiversx-sdk/vendor-rust

pytest .
```
