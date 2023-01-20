
import json
import logging
import subprocess
from pathlib import Path
from typing import List

from multiversx_sdk_rust_contract_builder.constants import (
    CONTRACT_CONFIG_FILENAME, OLD_CONTRACT_CONFIG_FILENAME)
from multiversx_sdk_rust_contract_builder.errors import ErrKnown


def is_source_code_file(path: Path) -> bool:
    if path.suffix == ".rs":
        return True
    if path.parent.name == "meta" and path.name == "Cargo.lock":
        return False
    if path.name in ["Cargo.toml", "Cargo.lock", CONTRACT_CONFIG_FILENAME, OLD_CONTRACT_CONFIG_FILENAME]:
        return True
    return False


def get_local_dependencies(contract_folder: Path, contract_name: str) -> List[Path]:
    logging.info(f"get_local_dependencies({contract_folder})")

    args = ["cargo", "metadata", "--format-version=1"]
    metadata_json = subprocess.check_output(args, cwd=contract_folder, shell=False, universal_newlines=True)
    metadata = json.loads(metadata_json)
    packages = metadata.get("packages", [])

    contract_package = next((package for package in packages if package["name"] == contract_name), None)
    if not contract_package:
        raise ErrKnown(f"Could not find contract {contract_name} in project metadata.")

    project_dependencies = contract_package.get("dependencies", [])
    local_dependencies = [depedency for depedency in project_dependencies if "path" in depedency]
    paths = [Path(dependency["path"]) for dependency in local_dependencies]
    return paths
