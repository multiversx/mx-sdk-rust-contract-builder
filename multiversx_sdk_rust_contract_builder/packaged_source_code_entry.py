
import base64
from pathlib import Path
from typing import Any, Dict, Optional, Protocol


class ISourceCodeFile(Protocol):
    path: Path
    module: Optional[Path]
    dependency_depth: Optional[int]


class PackagedSourceCodeEntry:
    def __init__(self, path: Path, content: bytes, module: Optional[Path], dependency_depth: Optional[int]) -> None:
        self.path = path
        self.content = content
        self.module = module
        self.dependency_depth = dependency_depth

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> 'PackagedSourceCodeEntry':
        path = Path(dict.get("path", ""))
        content = base64.b64decode(dict.get("content", ""))
        module = Path(dict.get("module", ""))
        dependency_depth = dict.get("dependency_depth", None)

        return PackagedSourceCodeEntry(path, content, module, dependency_depth)

    @classmethod
    def from_source_code_file(cls, project_folder: Path, source_code_file: ISourceCodeFile) -> 'PackagedSourceCodeEntry':
        path = source_code_file.path.relative_to(project_folder)
        content = Path(source_code_file.path).read_bytes()
        module = source_code_file.module.relative_to(project_folder) if source_code_file.module else None
        dependency_depth = source_code_file.dependency_depth

        return PackagedSourceCodeEntry(path, content, module, dependency_depth)

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "path": str(self.path),
            "content": base64.b64encode(self.content).decode(),
            "module": str(self.module),
            "dependencyDepth": self.dependency_depth,
        }

        return data
