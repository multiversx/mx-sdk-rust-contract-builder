import shutil
from pathlib import Path


def promote_cargo_lock_to_contract_directory(build_directory: Path, contract_directory: Path):
    from_path = build_directory / "wasm" / "Cargo.lock"
    to_path = contract_directory / "wasm" / "Cargo.lock"
    shutil.copy(from_path, to_path)
