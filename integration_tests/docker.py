
import os
import subprocess
from pathlib import Path
from typing import List, Optional


def run_docker(
    cargo_target_dir: Path,
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
