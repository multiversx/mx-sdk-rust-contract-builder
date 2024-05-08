import os
import shutil

from integration_tests.config import PARENT_OUTPUT_FOLDER
from integration_tests.shared import download_project_repository, run_docker
from multiversx_sdk_rust_contract_builder.packaged_source_code import \
    PackagedSourceCode


def test_with_symlinks():
    workspace_parent = download_project_repository("https://github.com/multiversx/mx-contracts-rs/archive/refs/tags/v0.45.4.zip", "test_with_symlinks")
    workspace = workspace_parent / "mx-contracts-rs-0.45.4"

    output_folder = PARENT_OUTPUT_FOLDER / "test_with_symlinks"
    shutil.rmtree(output_folder, ignore_errors=True)
    output_folder.mkdir(parents=True, exist_ok=True)

    # In the workspace, create a symlink towards something outside it:
    dummy_file = workspace_parent / "dummy"
    dummy_file.write_text("dummy")
    os.symlink(dummy_file, workspace / "dummy")

    # But also a symlink towards something inside the workspace:
    os.symlink(workspace / ".github", workspace / "github_symlink", target_is_directory=True)

    # Symlinks should be ignored, and the build should succeed.
    run_docker(
        project_path=workspace,
        packaged_src_path=None,
        contract_name="adder",
        image="sdk-rust-contract-builder:next",
        output_folder=output_folder
    )

    assert (output_folder / "artifacts.json").exists()


def test_has_correct_packaged_source():
    workspace_parent = download_project_repository("https://github.com/multiversx/mx-contracts-rs/archive/refs/tags/v0.45.4.zip", "test_with_symlinks")
    workspace = workspace_parent / "mx-contracts-rs-0.45.4"

    output_folder = PARENT_OUTPUT_FOLDER / "test_has_correct_packaged_source"
    shutil.rmtree(output_folder, ignore_errors=True)
    output_folder.mkdir(parents=True, exist_ok=True)

    run_docker(
        project_path=workspace,
        packaged_src_path=None,
        contract_name="adder",
        image="sdk-rust-contract-builder:next",
        output_folder=output_folder
    )

    packaged_source_code = PackagedSourceCode.from_file(output_folder / "adder" / "adder-0.0.0.source.json")

    for entry in packaged_source_code.entries:
        assert not str(entry.path).startswith("target"), f"Unexpected file: {entry.path}"
        assert entry.is_test_file == ("test" in str(entry.path)), f"Unexpected is_test_file marker for: {entry.path}"
