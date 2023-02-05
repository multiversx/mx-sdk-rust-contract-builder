
import json
from pathlib import Path
from typing import Any, Dict, Protocol

from multiversx_sdk_rust_contract_builder.cargo_toml import \
    get_contract_name_and_version
from multiversx_sdk_rust_contract_builder.filesystem import find_file_in_folder


class IWithToDict(Protocol):
    def to_dict(self) -> Dict[str, Any]: ...


class BuildOutcome:
    def __init__(self, build_metadata: IWithToDict, build_options: IWithToDict):
        self.contracts: Dict[str, BuildOutcomeEntry] = dict()
        self.build_metadata = build_metadata
        self.build_options = build_options

    def gather_artifacts(self, contract_name: str, build_folder: Path, output_subfolder: Path):
        self.contracts[contract_name] = BuildOutcomeEntry.from_folders(build_folder, output_subfolder)

    def get_entry(self, contract_name: str) -> 'BuildOutcomeEntry':
        return self.contracts[contract_name]

    def save_to_file(self, file: Path):
        data = self.to_dict()

        with open(file, "w") as f:
            json.dump(data, f, indent=4)

    def to_dict(self) -> Dict[str, Any]:
        contracts: Dict[str, Any] = {}

        for key, value in self.contracts.items():
            contracts[key] = value.to_dict()

        return {
            "buildMetadata": self.build_metadata.to_dict(),
            "buildOptions": self.build_options.to_dict(),
            "contracts": contracts
        }


class BuildOutcomeEntry:
    def __init__(self) -> None:
        self.version = ""
        self.codehash = ""
        self.artifacts = BunchOfBuildArtifacts()

    @classmethod
    def from_folders(cls, build_folder: Path, output_folder: Path) -> 'BuildOutcomeEntry':
        entry = BuildOutcomeEntry()
        _, entry.version = get_contract_name_and_version(build_folder)
        entry.codehash = find_file_in_folder(output_folder, "*.codehash.txt").read_text()
        entry.artifacts = BunchOfBuildArtifacts.from_output_folder(output_folder)
        return entry

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "codehash": self.codehash,
            "artifacts": self.artifacts.to_dict()
        }


class BunchOfBuildArtifacts:
    def __init__(self) -> None:
        self.bytecode = BuildArtifact(Path(""))
        self.abi = BuildArtifact(Path(""))
        self.src_package = BuildArtifact(Path(""))

    @classmethod
    def from_output_folder(cls, output_folder: Path) -> 'BunchOfBuildArtifacts':
        artifacts = BunchOfBuildArtifacts()
        artifacts.bytecode = BuildArtifact.find_in_output("*.wasm", output_folder)
        artifacts.abi = BuildArtifact.find_in_output("*.abi.json", output_folder)
        artifacts.src_package = BuildArtifact.find_in_output("*.source.json", output_folder)

        return artifacts

    def to_dict(self) -> Dict[str, str]:
        return {
            "bytecode": self.bytecode.path.name,
            "abi": self.abi.path.name,
            "srcPackage": self.src_package.path.name,
        }


class BuildArtifact:
    def __init__(self, path: Path) -> None:
        self.path = path

    @classmethod
    def find_in_output(cls, name_pattern: str, output_folder: Path) -> 'BuildArtifact':
        path = find_file_in_folder(output_folder, name_pattern)
        return BuildArtifact(path)

    def read(self) -> bytes:
        with open(self.path, "rb") as f:
            return f.read()
