import json
import shutil
import sys
import urllib.request
from pathlib import Path
from typing import List, Optional, Tuple

from integration_tests.docker import run_docker
from integration_tests.previous_builds import PreviousBuild, previous_builds

downloads_folder = Path("./testdata/downloads").resolve()
extracted_folder = Path("./testdata/input/extracted").resolve()
parent_output_folder = Path("./testdata/output").resolve()
cargo_target_dir = Path("./testdata/output/cargo_target_dir").resolve()


def main(cli_args: List[str]):
    shutil.rmtree(downloads_folder, ignore_errors=True)
    shutil.rmtree(extracted_folder, ignore_errors=True)
    shutil.rmtree(parent_output_folder, ignore_errors=True)

    downloads_folder.mkdir(parents=True, exist_ok=True)
    extracted_folder.mkdir(parents=True, exist_ok=True)
    cargo_target_dir.mkdir(parents=True, exist_ok=True)

    selected_builds = ["a.1", "a.2", "a.3", "b.1", "b.2", "b.3", "c.1", "c.2", "c.3", "c.4", "c.5", "d.1", "e.1"]

    for build in previous_builds:
        if not build.name in selected_builds:
            continue

        print("Reproducing build", build.name, "...")

        project_path, packaged_src_path = fetch_source_code(build)
        output_folder = parent_output_folder / build.name
        output_folder.mkdir(parents=True, exist_ok=True)

        if project_path and build.project_path_adjustment:
            project_path = project_path / build.project_path_adjustment

        run_docker(cargo_target_dir, project_path, packaged_src_path, build.contract_name, build.docker_image, output_folder)

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


if __name__ == "__main__":
    main(sys.argv[1:])
