
from pathlib import Path


def is_source_code_file(path: Path):
    if path.suffix == ".rs":
        return True
    if path.parent.name == "meta" and path.name == "Cargo.lock":
        return False
    if path.name in ["Cargo.toml", "Cargo.lock", "elrond.json"]:
        return True
    return False
