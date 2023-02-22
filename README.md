# mx-sdk-rust-contract-builder

Docker image (and wrappers) for reproducible contract builds (Rust). See [docs.multiversx.com](https://docs.multiversx.com/developers/reproducible-contract-builds/).

## Build the Docker image

We use `docker buildx` to build the image:

```
docker buildx build --output type=docker . -t sdk-rust-contract-builder:next -f ./Dockerfile
```

Maintainers can publish the image as follows:

```
docker buildx create --name multiarch --use

docker buildx build --push --platform=linux/amd64 . -t multiversx/sdk-rust-contract-builder:next -f ./Dockerfile

docker buildx rm multiarch
```

For the above to work properly, make sure to install `tonistiigi/binfmt` beforehand. Please follow the official Docker documentation [here](https://docs.docker.com/build/building/multi-platform/).

Note that **we only build and publish the image for `linux/amd64`**. We recommend against using a `linux/arm64` image for performing reproducible contract builds. This is because a WASM binary generated on the `linux/arm64` image _might_ differ (at the bytecode level) from one generated on the `linux/amd64` image - probably due to distinct (unfortunate) bytecode-emitting logic in the Rust compiler.

## Build contract using the wrapper

If you are using a Mac with ARM64, we _recommend_ setting the following variable beforehand (contract builds will be slower, but this eliminates the risk of not being able to reproduce the build on Linux):

```
export DOCKER_DEFAULT_PLATFORM=linux/amd64
```

Building from a project folder:

```
python3 ./build_with_docker.py --image=sdk-rust-contract-builder:next \
    --project=~/contracts/example \
    --output=~/contracts/output-from-docker
```

Building from a packaged source code:

```
python3 ./build_with_docker.py --image=sdk-rust-contract-builder:next \
    --packaged-src=~/contracts/example-0.0.0.source.json \
    --output=~/contracts/output-from-docker
```

## Run unit tests

```
pytest .
```

## Run integration tests (with Docker)

```
python3 ./integration_tests/test_previous_builds_are_reproducible.py --selected-builds "a.1" [...]
python3 ./integration_tests/test_project_folder_and_packaged_src_are_equivalent.py
```
