from pathlib import Path
from typing import Tuple

import toml


def get_contract_name_and_version(contract_folder: Path) -> Tuple[str, str]:
    file = contract_folder / "Cargo.toml"
    data = toml.loads(file.read_text())

    name = data["package"]["name"]
    version = data["package"]["version"]
    return name, version
