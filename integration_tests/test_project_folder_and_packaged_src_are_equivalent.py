import shutil
import sys
from pathlib import Path
from typing import List

from integration_tests.config import PARENT_OUTPUT_FOLDER
from integration_tests.shared import download_project_repository, run_docker


def main(cli_args: List[str]):
    repository_url = "https://github.com/multiversx/mx-reproducible-contract-build-example-sc"
    tag = "0.4.7"
    archve_subfolder = f"mx-reproducible-contract-build-example-sc-{tag}"
    project_path = download_project_repository(f"{repository_url}/archive/refs/tags/v{tag}.zip", archve_subfolder)
    project_path = project_path / archve_subfolder

    # Only package_whole_project_src = True works.
    # package_whole_project_src = False does not work, since a missing Cargo.lock at the workspace level leads to build errors.
    check_project_folder_and_packaged_src_are_equivalent(
        project_path=project_path,
        package_whole_project_src=True,
        parent_output_folder=PARENT_OUTPUT_FOLDER,
        contracts=["adder", "multisig"],
    )


def check_project_folder_and_packaged_src_are_equivalent(
        project_path: Path,
        package_whole_project_src: bool,
        parent_output_folder: Path,
        contracts: List[str]):
    for contract in contracts:
        output_using_project = parent_output_folder / "using-project" / contract / ("whole" if package_whole_project_src else "truncated")
        output_using_packaged_src = parent_output_folder / "using-packaged-src" / contract / ("whole" if package_whole_project_src else "truncated")

        shutil.rmtree(output_using_project, ignore_errors=True)
        shutil.rmtree(output_using_packaged_src, ignore_errors=True)

        output_using_project.mkdir(parents=True, exist_ok=True)
        output_using_packaged_src.mkdir(parents=True, exist_ok=True)

        run_docker(
            project_path=project_path,
            package_whole_project_src=package_whole_project_src,
            packaged_src_path=None,
            contract_name=contract,
            image="sdk-rust-contract-builder:next",
            output_folder=output_using_project
        )

        packaged_src_path = output_using_project / f"{contract}/{contract}-0.0.0.source.json"

        run_docker(
            project_path=None,
            package_whole_project_src=package_whole_project_src,
            packaged_src_path=packaged_src_path,
            contract_name=contract,
            image="sdk-rust-contract-builder:next",
            output_folder=output_using_packaged_src
        )

        # Check that output folders are identical
        using_project_output_files = sorted((output_using_project / contract).rglob("*"))
        using_packaged_src_output_files = sorted((output_using_packaged_src / contract).rglob("*"))

        assert len(using_project_output_files) == len(using_packaged_src_output_files)

        for index, file_using_project in enumerate(using_project_output_files):
            file_using_packaged_src = using_packaged_src_output_files[index]

            if not file_using_project.is_file() or file_using_project.suffix == ".zip":
                continue
            file_content_using_project = file_using_project.read_bytes()
            file_content_using_packaged_src = file_using_packaged_src.read_bytes()

            if file_content_using_project == file_content_using_packaged_src:
                print(f"Files are identical ({contract}): {file_using_project.name}")
            else:
                print(f"Files differ ({contract}):")
                print(f"  {file_using_project}")
                print(f"  {file_using_packaged_src}")
                raise Exception(f"Files differ ({contract}): {file_using_project.name}")


if __name__ == "__main__":
    main(sys.argv[1:])
