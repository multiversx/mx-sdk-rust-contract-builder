import json
import shutil
import sys
import urllib.request
import os
import subprocess
from pathlib import Path
from typing import List, Optional

from integration_tests.config import DOWNLOADS_FOLDER, EXTRACTED_FOLDER, PARENT_OUTPUT_FOLDER, CARGO_TARGET_DIR


def download_repository(zip_archive_url: str, name: str) -> Path:
    downloaded_archive = DOWNLOADS_FOLDER / f"{name}.zip"
    extracted_project = EXTRACTED_FOLDER / name
    urllib.request.urlretrieve(zip_archive_url, downloaded_archive)
    shutil.unpack_archive(downloaded_archive, extracted_project)
    return extracted_project


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

    docker_mount_args += ["--volume", f"{CARGO_TARGET_DIR}:/rust/cargo-target-dir"]

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
