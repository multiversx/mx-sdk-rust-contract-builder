import json
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Tuple

downloads_folder = Path("./testdata/downloads").resolve()
extracted_folder = Path("./testdata/input/extracted").resolve()
parent_output_folder = Path("./testdata/output").resolve()
cargo_target_dir = Path("./testdata/output/cargo_target_dir").resolve()


class PreviousBuild:
    def __init__(self, name: str,
                 project_zip_url: Optional[str],
                 project_path_adjustment: Optional[str],
                 packaged_src_url: Optional[str],
                 contract_name: Optional[str],
                 expected_code_hashes: Dict[str, str],
                 docker_image: str) -> None:
        self.name = name
        self.project_zip_url = project_zip_url
        self.project_path_adjustment = project_path_adjustment
        self.packaged_src_url = packaged_src_url
        self.contract_name = contract_name
        self.expected_code_hashs = expected_code_hashes
        self.docker_image = docker_image


builds: List[PreviousBuild] = [
    PreviousBuild(
        name="a.1",
        project_zip_url="https://github.com/multiversx/mx-reproducible-contract-build-example-sc/archive/refs/tags/v0.1.5.zip",
        project_path_adjustment=None,
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "adder": "58c6e78f40bd6ccc30d8a01f952b34a13ebfdad796a2526678be17c5d7820174"
        },
        docker_image="elrondnetwork/build-contract-rust:v3.0.0"
    ),
    PreviousBuild(
        name="a.2",
        project_zip_url="https://github.com/multiversx/mx-reproducible-contract-build-example-sc/archive/refs/tags/v0.1.5.zip",
        project_path_adjustment=None,
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "adder": "58c6e78f40bd6ccc30d8a01f952b34a13ebfdad796a2526678be17c5d7820174"
        },
        docker_image="multiversx/sdk-rust-contract-builder:v4.0.3"
    ),
    PreviousBuild(
        name="a.3",
        project_zip_url="https://github.com/multiversx/mx-reproducible-contract-build-example-sc/archive/refs/tags/v0.1.5.zip",
        project_path_adjustment=None,
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "adder": "58c6e78f40bd6ccc30d8a01f952b34a13ebfdad796a2526678be17c5d7820174"
        },
        docker_image="sdk-rust-contract-builder:next"
    ),
    PreviousBuild(
        name="b.1",
        project_zip_url="https://github.com/multiversx/mx-exchange-sc/archive/refs/tags/v1.5.4-metabonding-unbond.zip",
        project_path_adjustment="mx-exchange-sc-1.5.4-metabonding-unbond",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "metabonding-staking": "4a9b2afa13eca738b1804c48b82a961afd67adcbbf2aa518052fa124ac060bea"
        },
        docker_image="elrondnetwork/build-contract-rust:v3.1.0"
    ),
    PreviousBuild(
        name="b.2",
        project_zip_url="https://github.com/multiversx/mx-exchange-sc/archive/refs/tags/v1.5.4-metabonding-unbond.zip",
        project_path_adjustment="mx-exchange-sc-1.5.4-metabonding-unbond",
        packaged_src_url=None,
        contract_name="metabonding-staking",
        expected_code_hashes={
            "metabonding-staking": "4a9b2afa13eca738b1804c48b82a961afd67adcbbf2aa518052fa124ac060bea"
        },
        docker_image="elrondnetwork/build-contract-rust:v3.2.0"
    ),
    PreviousBuild(
        name="b.3",
        project_zip_url="https://github.com/multiversx/mx-exchange-sc/archive/refs/tags/v1.5.4-metabonding-unbond.zip",
        project_path_adjustment="mx-exchange-sc-1.5.4-metabonding-unbond",
        packaged_src_url=None,
        contract_name="metabonding-staking",
        expected_code_hashes={
            "metabonding-staking": "4a9b2afa13eca738b1804c48b82a961afd67adcbbf2aa518052fa124ac060bea"
        },
        docker_image="multiversx/sdk-rust-contract-builder:v3.2.3"
    )
]


def main(cli_args: List[str]):
    shutil.rmtree(downloads_folder, ignore_errors=True)
    shutil.rmtree(extracted_folder, ignore_errors=True)
    shutil.rmtree(parent_output_folder, ignore_errors=True)

    downloads_folder.mkdir(parents=True, exist_ok=True)
    extracted_folder.mkdir(parents=True, exist_ok=True)
    cargo_target_dir.mkdir(parents=True, exist_ok=True)

    for build in builds:
        print("Reproducing build", build.name, "...")

        project_path, packaged_src_path = fetch_source_code(build)
        output_folder = parent_output_folder / build.name
        output_folder.mkdir(parents=True, exist_ok=True)

        if project_path and build.project_path_adjustment:
            project_path = project_path / build.project_path_adjustment

        run_docker(project_path, packaged_src_path, build.contract_name, build.docker_image, output_folder)

        artifacts_path = output_folder / "artifacts.json"
        artifacts_json = artifacts_path.read_text()
        artifacts = json.loads(artifacts_json)

        for contract_name, expected_code_hash in build.expected_code_hashs.items():
            print(f"For contract {contract_name}, expecting code hash {expected_code_hash} ...")
            codehash = artifacts[contract_name]["codehash"]
            if len(codehash) != 64:
                # It's an older image, "artifacts.json" contains a path towards the code hash, instead of the actual code hash
                codehash = Path(output_folder / contract_name / codehash).read_text().strip()

            if codehash != expected_code_hash:
                raise Exception(f"{build.name}: codehash mismatch for contract {contract_name}! Expected {expected_code_hash}, got {codehash}")
            print("OK, codehash matches!", codehash)


def fetch_source_code(build: PreviousBuild) -> Tuple[Optional[Path], Optional[Path]]:
    print("Fetching source code for", build.name, "...")

    if build.project_zip_url:
        downloaded_archive = downloads_folder / f"{build.name}.zip"
        extracted_project = extracted_folder / build.name
        urllib.request.urlretrieve(build.project_zip_url, downloaded_archive)
        shutil.unpack_archive(downloaded_archive, extracted_project)
        return extracted_project, None

    if build.packaged_src_url:
        downloaded_packaged_src = downloads_folder / f"{build.name}.json"
        urllib.request.urlretrieve(build.packaged_src_url, downloaded_packaged_src)
        return None, downloaded_packaged_src

    raise Exception("No source code provided")


def run_docker(
        project_path: Optional[Path],
        packaged_src_path: Optional[Path],
        contract_name: Optional[str],
        image: str,
        output_folder: Path,
):
    docker_mount_args: List[str] = ["--volume", f"{output_folder}:/output"]

    if project_path:
        docker_mount_args.extend(["--volume", f"{project_path}:/project"])

    if packaged_src_path:
        docker_mount_args.extend(["--volume", f"{packaged_src_path}:/packaged-src.json"])

    docker_mount_args += ["--volume", f"{cargo_target_dir}:/rust/cargo-target-dir"]

    docker_args = ["docker", "run"]
    docker_args += docker_mount_args
    docker_args += ["--user", f"{str(os.getuid())}:{str(os.getgid())}"]
    docker_args += ["--rm", image]

    entrypoint_args: List[str] = []

    if project_path:
        entrypoint_args.extend(["--project", "project"])

    if packaged_src_path:
        entrypoint_args.extend(["--packaged-src", "packaged-src.json"])

    if contract_name:
        entrypoint_args.extend(["--contract", contract_name])

    args = docker_args + entrypoint_args

    result = subprocess.run(args)
    return result.returncode


if __name__ == "__main__":
    main(sys.argv[1:])
