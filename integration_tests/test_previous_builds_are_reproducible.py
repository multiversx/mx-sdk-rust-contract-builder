from argparse import ArgumentParser
import json
import shutil
import sys
import urllib.request
from pathlib import Path
from typing import List, Optional, Tuple
from integration_tests.config import DOWNLOADS_FOLDER, EXTRACTED_FOLDER, PARENT_OUTPUT_FOLDER, CARGO_TARGET_DIR
from integration_tests.shared import download_repository, run_docker
from integration_tests.previous_builds import PreviousBuild, previous_builds


def main(cli_args: List[str]):
    parser = ArgumentParser()
    parser.add_argument("--selected-builds", nargs='+')
    parsed_args = parser.parse_args(cli_args)
    selected_builds = parsed_args.selected_builds

    shutil.rmtree(DOWNLOADS_FOLDER, ignore_errors=True)
    shutil.rmtree(EXTRACTED_FOLDER, ignore_errors=True)
    shutil.rmtree(PARENT_OUTPUT_FOLDER, ignore_errors=True)

    DOWNLOADS_FOLDER.mkdir(parents=True, exist_ok=True)
    EXTRACTED_FOLDER.mkdir(parents=True, exist_ok=True)
    CARGO_TARGET_DIR.mkdir(parents=True, exist_ok=True)

    for build in previous_builds:
        if not build.name in selected_builds:
            continue

        print("Reproducing build", build.name, "...")

        project_path, packaged_src_path = fetch_source_code(build)
        output_folder = PARENT_OUTPUT_FOLDER / build.name
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
        return download_repository(build.project_zip_url, build.name), None
    if build.packaged_src_url:
        downloaded_packaged_src = DOWNLOADS_FOLDER / f"{build.name}.json"
        urllib.request.urlretrieve(build.packaged_src_url, downloaded_packaged_src)
        return None, downloaded_packaged_src

    raise Exception("No source code provided")


if __name__ == "__main__":
    main(sys.argv[1:])
