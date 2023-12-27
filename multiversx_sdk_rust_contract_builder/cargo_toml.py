import logging
import shutil
from pathlib import Path
from typing import Tuple

import toml

from multiversx_sdk_rust_contract_builder.filesystem import get_all_files


def get_contract_name_and_version(contract_folder: Path) -> Tuple[str, str]:
    file = contract_folder / "Cargo.toml"
    data = toml.loads(file.read_text())

    name = data["package"]["name"]
    version = data["package"]["version"]
    return name, version


def promote_cargo_lock_to_contract_folder(build_folder: Path, contract_folder: Path):
    from_path = build_folder / "wasm" / "Cargo.lock"
    to_path = contract_folder / "wasm" / "Cargo.lock"
    shutil.copy(from_path, to_path)


def remove_dev_dependencies_sections_from_all(folder: Path):
    logging.info(f"remove_dev_dependencies_sections_from_all({folder})")

    all_files = get_all_files(folder, lambda file: file.name == "Cargo.toml")
    for file in all_files:
        remove_dev_dependencies_sections(file)


def remove_dev_dependencies_sections(file: Path):
    data = toml.loads(file.read_text())

    if "dev-dependencies" in data:
        del data["dev-dependencies"]
        file.write_text(toml.dumps(data))
