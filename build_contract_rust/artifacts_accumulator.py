
import json
from pathlib import Path
from typing import Dict

from build_contract_rust.filesystem import find_file_in_folder


class ArtifactsAccumulator:
    def __init__(self):
        self.contracts: Dict[str, Dict[str, str]] = dict()

    def gather_artifacts(self, contract_name: str, output_subdirectory: Path):
        with open(find_file_in_folder(output_subdirectory, "*.codehash.txt")) as file:
            code_hash = file.read()

        self.add_artifact(contract_name, "bytecode", find_file_in_folder(output_subdirectory, "*.wasm").name)
        self.add_artifact(contract_name, "text", find_file_in_folder(output_subdirectory, "*.wat").name)
        self.add_artifact(contract_name, "abi", find_file_in_folder(output_subdirectory, "*.abi.json").name)
        self.add_artifact(contract_name, "imports", find_file_in_folder(output_subdirectory, "*.imports.json").name)
        self.add_artifact(contract_name, "codehash", code_hash)
        self.add_artifact(contract_name, "srcPackage", find_file_in_folder(output_subdirectory, "*.source.json").name)
        self.add_artifact(contract_name, "srcArchive", find_file_in_folder(output_subdirectory, "*-src-*.zip").name)
        self.add_artifact(contract_name, "src", find_file_in_folder(output_subdirectory, "*-src-*.zip").name)
        self.add_artifact(contract_name, "output", find_file_in_folder(output_subdirectory, "*-output-*.zip").name)

    def add_artifact(self, contract_name: str, kind: str, value: str):
        if contract_name not in self.contracts:
            self.contracts[contract_name] = dict()

        self.contracts[contract_name][kind] = value

    def dump_to_file(self, file: Path):
        with open(file, "w") as f:
            json.dump(self.contracts, f, indent=4)
