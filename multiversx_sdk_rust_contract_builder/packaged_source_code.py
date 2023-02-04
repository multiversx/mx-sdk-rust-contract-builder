
import base64
import json
from pathlib import Path
from typing import Any, Dict, List

from multiversx_sdk_rust_contract_builder.source_code import SourceCodeFile


class PackagedSourceCodeEntry:
    def __init__(self, path: Path, content: bytes) -> None:
        self.path = path
        self.content = content

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> 'PackagedSourceCodeEntry':
        path = Path(dict.get("path", ""))
        content = base64.b64decode(dict.get("content", ""))
        return PackagedSourceCodeEntry(path, content)

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "path": str(self.path),
            "content": base64.b64encode(self.content).decode()
        }

        return data


class PackagedSourceCode:
    def __init__(self, name: str, version: str, entries: List[PackagedSourceCodeEntry]) -> None:
        self.name = name
        self.version = version
        self.entries = entries

    @classmethod
    def from_file(cls, path: Path) -> 'PackagedSourceCode':
        with open(path, "r") as f:
            data: Dict[str, Any] = json.load(f)

        return PackagedSourceCode.from_dict(data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PackagedSourceCode':
        name = data.get("name", "untitled")
        version = data.get("version", "0.0.0")
        entries_raw: List[Dict[str, Any]] = data.get("entries", [])
        entries = [PackagedSourceCodeEntry.from_dict(entry) for entry in entries_raw]
        _sort_entries(entries)

        return PackagedSourceCode(name, version, entries)

    @classmethod
    def from_filesystem(cls, project_folder: Path, contract_name: str, contract_version: str, source_code_files: List[SourceCodeFile]) -> 'PackagedSourceCode':
        entries: List[PackagedSourceCodeEntry] = []

        for file in source_code_files:
            full_path = file.path
            content = full_path.read_bytes()
            relative_path = full_path.relative_to(project_folder)
            entries.append(PackagedSourceCodeEntry(relative_path, content))

        _sort_entries(entries)
        return PackagedSourceCode(contract_name, contract_version, entries)

    def unwrap_to_filesystem(self, project_folder: Path):
        for entry in self.entries:
            full_path = project_folder / entry.path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, "wb") as f:
                f.write(entry.content)

    def save_to_file(self, path: Path):
        data = self.to_dict()

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def to_dict(self) -> Dict[str, Any]:
        entries = [entry.to_dict() for entry in self.entries]

        return {
            "name": self.name,
            "version": self.version,
            "entries": entries
        }


def _sort_entries(entries: List[PackagedSourceCodeEntry]) -> List[PackagedSourceCodeEntry]:
    entries.sort(key=lambda entry: entry.path)
    return entries
