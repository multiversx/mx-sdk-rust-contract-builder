import os
import shutil
import subprocess
import urllib.request
from pathlib import Path
from typing import List, Optional

from integration_tests.config import (CARGO_TARGET_DIR, DOWNLOADS_FOLDER,
                                      EXTRACTED_FOLDER)


def download_project_repository(zip_archive_url: str, name: str) -> Path:
    DOWNLOADS_FOLDER.mkdir(parents=True, exist_ok=True)
    EXTRACTED_FOLDER.mkdir(parents=True, exist_ok=True)

    download_to_path = DOWNLOADS_FOLDER / f"{name}.zip"
    extract_to_path = EXTRACTED_FOLDER / name

    urllib.request.urlretrieve(zip_archive_url, download_to_path)
    shutil.rmtree(extract_to_path, ignore_errors=True)
    shutil.unpack_archive(download_to_path, extract_to_path)
    return extract_to_path


def download_packaged_src(json_url: str, name: str) -> Path:
    downloaded_packaged_src = DOWNLOADS_FOLDER / f"{name}.source.json"
    urllib.request.urlretrieve(json_url, downloaded_packaged_src)


def run_docker(
    project_path: Optional[Path],
    packaged_src_path: Optional[Path],
    contract_name: Optional[str],
    image: str,
    output_folder: Path,
):
    CARGO_TARGET_DIR.mkdir(parents=True, exist_ok=True)

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
    returncode = result.returncode
    if returncode != 0:
        raise Exception(f"Docker exited with return code {returncode}.")
