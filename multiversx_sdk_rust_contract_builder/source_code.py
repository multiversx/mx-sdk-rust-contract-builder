
import json
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


def get_local_dependencies_wildcards(contract_folder: Path) -> List[str]:
    new_config_file = contract_folder / CONTRACT_CONFIG_FILENAME
    old_config_file = contract_folder / OLD_CONTRACT_CONFIG_FILENAME

    if new_config_file.exists():
        config_file = new_config_file
    elif old_config_file.exists():
        config_file = old_config_file
    else:
        raise ErrKnown(f"Could not find contract config file in {contract_folder}")

    config_content = config_file.read_text()
    config = json.loads(config_content)
    wildcards = config.get("localDependencies", [])
    return wildcards
