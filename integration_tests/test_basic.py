import os
import shutil

from integration_tests.config import PARENT_OUTPUT_FOLDER
from integration_tests.shared import download_project_repository, run_docker


def test_with_symlinks():
    workspace_parent = download_project_repository("https://github.com/multiversx/mx-contracts-rs/archive/refs/tags/v0.45.2.2.zip", "test_with_symlinks")
    workspace = workspace_parent / "mx-contracts-rs-0.45.2.2"

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
