
import json
import logging
import subprocess
from pathlib import Path
from typing import List

from multiversx_sdk_rust_contract_builder.constants import (
    CONTRACT_CONFIG_FILENAME, OLD_CONTRACT_CONFIG_FILENAME)
from multiversx_sdk_rust_contract_builder.errors import ErrKnown
from multiversx_sdk_rust_contract_builder.filesystem import get_all_files


class SourceCodeFile:
    def __init__(self, path: Path, module: Path, dependency_depth: int):
        self.path = path
        self.module = module
        self.dependency_depth = dependency_depth
        self.is_test_file = is_test_file(path)


def get_all_source_code_files(folder: Path) -> List[Path]:
    return sorted(get_all_files(folder, is_source_code_file))


def is_source_code_file(path: Path) -> bool:
    if path.suffix == ".rs":
        return True
    if path.parent.name == "meta" and path.name == "Cargo.lock":
        return False
    if path.name in ["Cargo.toml", "Cargo.lock", CONTRACT_CONFIG_FILENAME, OLD_CONTRACT_CONFIG_FILENAME]:
        return True
    return False


def replace_all_test_content_with_noop(folder: Path, content: str):
    return
    # At this moment (January 2023) we cannot completely exclude test files from the compilation
    # (if we do so, the build throws some errors, in some cases).
    # So we replace all test content with a noop function.
    # This is not ideal, but it works for now.

    logging.info(f"replace_all_test_content_with_noop({folder})")
    test_files = get_all_files(folder, is_test_file)
    for file in test_files:
        file.write_text(content)


def is_test_file(path: Path) -> bool:
    is_in_tests_folder = any(part in ["test", "tests"] for part in path.parts)
    return path.suffix == ".rs" and is_in_tests_folder


def get_source_code_files_necessary_for_contract_v2(project_folder: Path, contract_folder: Path) -> List[SourceCodeFile]:
    args = ["sc-meta", "local-deps", "--path", str(contract_folder)]
    logging.info(f"get_source_code_files_necessary_for_contract_v2(), running: {args}")
    subprocess.check_output(args, shell=False, universal_newlines=True, cwd=project_folder)

    output_file = contract_folder / "output" / "local_deps.txt"
    output_content = output_file.read_text()

    data = json.loads(output_content)
    dependencies = data.get("dependencies", [])

    source_code_files: List[SourceCodeFile] = []

    for dependency in dependencies:
        dependency_path = (contract_folder / dependency.get("path", "")).resolve()
        dependency_depth = dependency.get("depth", 0)

        if not dependency_path.exists():
            raise ErrKnown(f"Dependency does not exist: {dependency_path}")

        files_of_dependency = get_all_files(dependency_path, is_source_code_file)

        for file in files_of_dependency:
            source_code_file = SourceCodeFile(file, dependency_path, dependency_depth)
            source_code_files.append(source_code_file)

    files_of_contract = get_all_files(contract_folder, is_source_code_file)
    for file in files_of_contract:
        source_code_file = SourceCodeFile(file, contract_folder, 0)
        source_code_files.append(source_code_file)

    return source_code_files
