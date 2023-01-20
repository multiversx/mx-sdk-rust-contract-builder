
import shutil
from pathlib import Path
from typing import Tuple


def get_contract_name_and_version(contract_folder: Path) -> Tuple[str, str]:
    # For simplicity and less dependencies installed in the Docker image, we do not rely on an external library
    # to parse the metadata from Cargo.toml.
    with open(contract_folder / "Cargo.toml") as file:
        lines = file.readlines()

    line_with_name = next((line for line in lines if line.startswith("name = ")), 'name = "untitled"')
    line_with_version = next((line for line in lines if line.startswith("version = ")), 'version = "0.0.0"')

    name = line_with_name.split("=")[1].strip().strip('"')
    version = line_with_version.split("=")[1].strip().strip('"')
    return name, version


def promote_cargo_lock_to_contract_folder(build_folder: Path, contract_folder: Path):
    from_path = build_folder / "wasm" / "Cargo.lock"
    to_path = contract_folder / "wasm" / "Cargo.lock"
    shutil.copy(from_path, to_path)
