
from pathlib import Path

from multiversx_sdk_rust_contract_builder.constants import (
    OLD_PROJECT_CONFIG_FILENAME, PROJECT_CONFIG_FILENAME)


def is_source_code_file(path: Path):
    if path.suffix == ".rs":
        return True
    if path.parent.name == "meta" and path.name == "Cargo.lock":
        return False
    if path.name in ["Cargo.toml", "Cargo.lock", PROJECT_CONFIG_FILENAME, OLD_PROJECT_CONFIG_FILENAME]:
        return True
    return False
