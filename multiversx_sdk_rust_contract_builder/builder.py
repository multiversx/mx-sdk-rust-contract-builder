import logging
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List

from multiversx_sdk_rust_contract_builder import cargo_toml, source_code
from multiversx_sdk_rust_contract_builder.build_metadata import BuildMetadata
from multiversx_sdk_rust_contract_builder.build_options import BuildOptions
from multiversx_sdk_rust_contract_builder.build_outcome import BuildOutcome
from multiversx_sdk_rust_contract_builder.cargo_toml import (
    get_contract_name_and_version, promote_cargo_lock_to_contract_folder)
from multiversx_sdk_rust_contract_builder.codehash import \
    generate_code_hash_artifact
from multiversx_sdk_rust_contract_builder.constants import (
    CONTRACT_CONFIG_FILENAME, MAX_PACKAGED_SOURCE_CODE_SIZE,
    OLD_CONTRACT_CONFIG_FILENAME)
from multiversx_sdk_rust_contract_builder.errors import ErrKnown
from multiversx_sdk_rust_contract_builder.filesystem import find_file_in_folder
from multiversx_sdk_rust_contract_builder.packaged_source_code import (
    PackagedSourceCode, PackagedSourceMetadata)


def build_project(
    project_folder: Path,
    parent_output_folder: Path,
    metadata: BuildMetadata,
    options: BuildOptions
) -> BuildOutcome:
    project_folder = project_folder.expanduser().resolve()
    parent_output_folder = parent_output_folder.expanduser().resolve()
    cargo_target_dir = options.cargo_target_dir.expanduser().resolve()
    package_whole_project_src = options.package_whole_project_src
    no_wasm_opt = options.no_wasm_opt
    specific_contract = options.specific_contract
    build_root_folder = options.build_root_folder

    ensure_output_folder_is_empty(parent_output_folder)

    outcome = BuildOutcome(metadata, options)
    contracts_folders = get_contracts_folders(project_folder)

    # We copy the whole project folder to the build path, to ensure that all local dependencies are available.
    project_within_build_folder = copy_project_folder_to_build_folder(project_folder, build_root_folder)

    if not package_whole_project_src:
        cargo_toml.remove_dev_dependencies_sections_from_all(project_within_build_folder)

    for contract_folder in sorted(contracts_folders):
        contract_name, contract_version = get_contract_name_and_version(contract_folder)
        logging.info(f"Contract = {contract_name}, version = {contract_version}")

        if specific_contract and contract_name != specific_contract:
            logging.info(f"Skipping {contract_name}.")
            continue

        output_subfolder = parent_output_folder / f"{contract_name}"
        output_subfolder.mkdir(parents=True, exist_ok=True)

        relative_contract_folder = contract_folder.relative_to(project_folder)
        contract_build_subfolder = project_within_build_folder / relative_contract_folder

        # Clean folder - it may contain externally-generated build artifacts
        clean_contract(contract_build_subfolder)
        build_contract(contract_build_subfolder, output_subfolder, cargo_target_dir, no_wasm_opt)

        # We do not clean the "output" folder, since it will be included in one of the generated archives.
        clean_contract(contract_build_subfolder, clean_output=False)

        # If this is the first build of the contract, Cargo.lock will be missing. We need to copy it from the container to host folder.
        promote_cargo_lock_to_contract_folder(contract_build_subfolder, contract_folder)

        # The bundle (packaged source code) is created after build, so that Cargo.lock files are included (if previously missing).
        create_packaged_source_code(
            parent_project_folder=project_within_build_folder,
            package_whole_project_src=package_whole_project_src,
            contract_folder=contract_build_subfolder,
            output_folder=output_subfolder,
            build_metadata=metadata.to_dict(),
            build_options=options.to_dict(),
        )

        outcome.gather_artifacts(contract_name, contract_build_subfolder, output_subfolder)

    return outcome


def ensure_output_folder_is_empty(parent_output_folder: Path):
    is_empty = len(os.listdir(parent_output_folder)) == 0
    if not is_empty:
        raise ErrKnown(f"Output folder must be empty: {parent_output_folder}")


def get_contracts_folders(project_path: Path) -> List[Path]:
    old_markers = list(project_path.glob(f"**/{OLD_CONTRACT_CONFIG_FILENAME}"))
    new_markers = list(project_path.glob(f"**/{CONTRACT_CONFIG_FILENAME}"))
    marker_files = old_markers + new_markers
    folders = [marker_file.parent for marker_file in marker_files]
    return sorted(folders)


def copy_project_folder_to_build_folder(project_folder: Path, build_root_folder: Path):
    shutil.rmtree(build_root_folder, ignore_errors=True)
    build_root_folder.mkdir()
    shutil.copytree(project_folder, build_root_folder, dirs_exist_ok=True)
    return build_root_folder


def clean_contract(folder: Path, clean_output: bool = True):
    logging.info(f"Cleaning: {folder}")

    # On a best-effort basis, remove folders that (usually) hold build artifacts
    shutil.rmtree(folder / "wasm" / "target", ignore_errors=True)
    shutil.rmtree(folder / "meta" / "target", ignore_errors=True)

    if clean_output:
        shutil.rmtree(folder / "output", ignore_errors=True)


def build_contract(build_folder: Path, output_folder: Path, cargo_target_dir: Path, no_wasm_opt: bool):
    cargo_output_folder = build_folder / "output"
    meta_folder = build_folder / "meta"
    cargo_lock = build_folder / "wasm" / "Cargo.lock"

    args = ["cargo", "run", "build"]
    args.extend(["--target-dir", str(cargo_target_dir)])
    args.extend(["--no-wasm-opt"] if no_wasm_opt else [])
    args.extend(["--verbose"])

    # If the lock file is missing, or it needs to be updated, Cargo will exit with an error.
    # See: https://doc.rust-lang.org/cargo/commands/cargo-build.html
    if cargo_toml.does_cargo_build_support_locked(build_folder) and cargo_lock.exists():
        args.append("--locked")

    logging.info(f"Building: {args}")
    return_code = subprocess.run(args, cwd=meta_folder).returncode
    if return_code != 0:
        raise ErrKnown(f"Failed to build contract {build_folder}. Return code: {return_code}.")

    wasm_file = find_file_in_folder(cargo_output_folder, "*.wasm")
    generate_code_hash_artifact(wasm_file)

    shutil.copytree(cargo_output_folder, output_folder, dirs_exist_ok=True)


def create_packaged_source_code(
        parent_project_folder: Path,
        package_whole_project_src: bool,
        contract_folder: Path,
        output_folder: Path,
        build_metadata: Dict[str, Any],
        build_options: Dict[str, Any]
):
    source_code_files = source_code.get_source_code_files(
        project_folder=parent_project_folder,
        contract_folder=contract_folder,
        include_unrelated_to_contract=package_whole_project_src
    )

    contract_name, contract_version = get_contract_name_and_version(contract_folder)
    metadata = PackagedSourceMetadata(
        contract_name=contract_name,
        contract_version=contract_version,
        build_metadata=build_metadata,
        build_options=build_options,
    )

    package = PackagedSourceCode.from_filesystem(metadata, parent_project_folder, source_code_files)
    package_path = output_folder / f"{contract_name}-{contract_version}.source.json"
    package.save_to_file(package_path)

    size_of_file = package_path.stat().st_size
    if size_of_file > MAX_PACKAGED_SOURCE_CODE_SIZE:
        warn_file_too_large(package_path, size_of_file, MAX_PACKAGED_SOURCE_CODE_SIZE)


def warn_file_too_large(path: Path, size: int, max_size: int):
    logging.warning(f"""File is too large (this might cause issues with using downstream applications, such as the contract build verification services):
file = {path}, size = {size}, maximum size = {max_size}""")
