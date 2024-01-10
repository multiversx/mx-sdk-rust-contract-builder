
import json
import logging
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

from multiversx_sdk_rust_contract_builder.constants import (
    CONTRACT_CONFIG_FILENAME, SC_META_LOCAL_DEPS_FILENAME)
from multiversx_sdk_rust_contract_builder.errors import ErrKnown
from multiversx_sdk_rust_contract_builder.filesystem import get_all_files
from multiversx_sdk_rust_contract_builder.source_code_file import \
    SourceCodeFile


def get_source_code_files(
        project_folder: Path,
        contract_folder: Path,
        include_unrelated_to_contract: bool
) -> List[SourceCodeFile]:
    """
    Returns the source code files of the specified contract.

    If `include_unrelated_to_contract` is True, also returns project files that are not strictly related to the specified contract.
    """
    source_code_files: List[SourceCodeFile] = []

    # First, add the contract itself
    files = get_all_files(contract_folder, _is_source_code_file)
    for file in files:
        source_code_files.append(SourceCodeFile(file, contract_folder, 0))

    # Then, add all local dependencies
    dependencies = _get_local_dependencies(project_folder, contract_folder)

    for dependency in dependencies:
        dependency_relative_path = dependency.get("path", "")
        dependency_folder = (contract_folder / dependency_relative_path).resolve()
        dependency_depth = dependency.get("depth", 0)

        if not dependency_folder.exists():
            raise ErrKnown(f"Dependency does not exist: {dependency_folder}")

        files = get_all_files(dependency_folder, _is_source_code_file)
        for file in files:
            source_code_files.append(SourceCodeFile(file, dependency_folder, dependency_depth))

    # Finally, add remaining files (unrelated to contract), if desired
    files_related_to_contract = set(file.path for file in source_code_files)

    if include_unrelated_to_contract:
        all_files = get_all_files(project_folder, _is_source_code_file)
        for file in all_files:
            if file not in files_related_to_contract:
                source_code_files.append(SourceCodeFile(file, contract_folder, sys.maxsize))

    return source_code_files


def _is_source_code_file(path: Path) -> bool:
    if path.suffix == ".rs":
        return True
    if path.name in ["Cargo.toml", "Cargo.lock", "multicontract.toml", "sc-config.toml", CONTRACT_CONFIG_FILENAME]:
        return True
    return False


def _get_local_dependencies(project_folder: Path, contract_folder: Path) -> List[Dict[str, Any]]:
    args = ["sc-meta", "local-deps", "--path", str(contract_folder)]
    logging.info(f"_get_local_dependencies(), running: {args}")
    subprocess.check_output(args, shell=False, universal_newlines=True, cwd=project_folder)

    output_file = contract_folder / "output" / SC_META_LOCAL_DEPS_FILENAME
    output_content = output_file.read_text()

    logging.debug(f"_get_local_dependencies() output:")
    logging.debug(output_content)

    data = json.loads(output_content)
    dependencies = data.get("dependencies", [])
    return dependencies
