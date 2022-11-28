# elrond-sdk-images-build-contract-rust

Docker image (and wrappers) for reproducible contract builds (Rust). See [docs.elrond.com](https://docs.elrond.com/developers/reproducible-contract-builds/).

## Build the Docker image

```
docker buildx build --no-cache . -t build-contract-rust:experimental -f ./Dockerfile
```

## Build contract using the wrapper

Without providing `cargo-target-dir`:

```
python3 ./build_with_docker.py --image=build-contract-rust:experimental \
    --project=~/contracts/reproducible-contract-build-example \
    --output=~/contracts/output-from-docker
```

With providing `cargo-target-dir`:

```
python3 ./build_with_docker.py --image=build-contract-rust:experimental \
    --project=~/contracts/reproducible-contract-build-example \
    --output=~/contracts/output-from-docker \
    --cargo-target-dir=~/cargo-target-dir-docker
```

Building from a packaged source code:

```
python3 ./build_with_docker.py --image=build-contract-rust:experimental \
    --packaged-src=~/contracts/example-0.0.0.source.json \
    --output=~/contracts/output-from-docker
```

## Build contract using the Docker inner script

This is useful for useful for testing, debugging and reviewing the script.

```
export PROJECT=${HOME}/contracts/reproducible-contract-build-example
export OUTPUT=${HOME}/contracts/output
export CARGO_TARGET_DIR=${HOME}/cargo-target-dir
export PATH=${HOME}/elrondsdk/vendor-rust/bin:${HOME}/elrondsdk/wabt/latest/bin:${PATH}
export RUSTUP_HOME=${HOME}/elrondsdk/vendor-rust
export CARGO_HOME=${HOME}/elrondsdk/vendor-rust
```

Build a project:

```
python3 ./build_within_docker.py --project=${PROJECT} --output=${OUTPUT} \
    --cargo-target-dir=${CARGO_TARGET_DIR}
```
