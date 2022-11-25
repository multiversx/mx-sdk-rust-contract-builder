
import json
from pathlib import Path
from typing import Any, Dict

from build_contract_rust.filesystem import find_file_in_folder


class BuildOutcome:
    def __init__(self):
        self.contracts: Dict[str, Dict[str, Any]] = dict()

    def gather_artifacts(self, contract_name: str, contract_version: str, output_subdirectory: Path):
        with open(find_file_in_folder(output_subdirectory, "*.codehash.txt")) as file:
            code_hash = file.read()

        self.contracts[contract_name] = {
            "version": contract_version,
            "codehash": code_hash,
            "artifacts": dict()
        }

        artifacts = self.contracts[contract_name]["artifacts"]
        artifacts["bytecode"] = find_file_in_folder(output_subdirectory, "*.wasm").name
        artifacts["text"] = find_file_in_folder(output_subdirectory, "*.wat").name
        artifacts["abi"] = find_file_in_folder(output_subdirectory, "*.abi.json").name
        artifacts["imports"] = find_file_in_folder(output_subdirectory, "*.imports.json").name
        artifacts["srcPackage"] = find_file_in_folder(output_subdirectory, "*.source.json").name
        artifacts["srcArchive"] = find_file_in_folder(output_subdirectory, "*-src-*.zip").name
        artifacts["src"] = find_file_in_folder(output_subdirectory, "*-src-*.zip").name
        artifacts["output"] = find_file_in_folder(output_subdirectory, "*-output-*.zip").name

    def get_version(self, contract_name: str) -> str:
        return self.contracts[contract_name]["version"]

    def get_codehash(self, contract_name: str) -> str:
        return self.contracts[contract_name]["codehash"]

    def load_artifact(self, contract_name: str, kind: str) -> bytes:
        path = Path(self.contracts[contract_name][kind])
        with open(path, "rb") as f:
            return f.read()

    def save_to_file(self, file: Path):
        with open(file, "w") as f:
            json.dump(self.contracts, f, indent=4)
