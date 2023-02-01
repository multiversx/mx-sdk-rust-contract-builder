import logging
import shutil
from pathlib import Path
from typing import Any, Tuple

import semver
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


def does_cargo_build_support_locked(contract_folder: Path) -> bool:
    file = contract_folder / "Cargo.toml"
    data: Any = toml.loads(file.read_text())

    framework_version_old: str = str(data.get("dependencies", {}).get("elrond-wasm", {}).get("version", ""))
    framework_version_new: str = str(data.get("dependencies", {}).get("multiversx-sc", {}).get("version", ""))
    framework_version: str = framework_version_old or framework_version_new
    framework_version = _normalize_rust_framework_version(framework_version)

    # Before this version, --locked was ignored.
    # On this version, using --locked resulted in an error.
    # After this version, --locked is supported.
    supports_locked: bool = semver.compare(framework_version, "0.39.2") > 0

    logging.info(f"does_cargo_build_support_locked({contract_folder}), framework version = {framework_version}? {supports_locked}")
    return supports_locked


def _normalize_rust_framework_version(version: str) -> str:
    version = version.strip('^').strip('=')
    version_parts = version.split(".")
    if len(version_parts) == 2:
        version += ".0"
    return version
