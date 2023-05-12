import logging
import shutil
import sys
from typing import List

from integration_tests.config import PARENT_OUTPUT_FOLDER
from integration_tests.shared import download_project_repository, run_docker


def main(cli_args: List[str]):
    logging.basicConfig(level=logging.DEBUG)

    # TODO: when possible, use multiversx/mx-exchange-sc (as of May 2023, it references mx-sdk-rs < v0.41.0, thus cannot be used for testing reproducible builds v5).
    project_path = download_project_repository("https://github.com/defralcoding/xBulk/archive/refs/heads/main.zip", "xBulk-main")

    parent_output_using_project = PARENT_OUTPUT_FOLDER / "using-project"
    parent_output_using_packaged_src = PARENT_OUTPUT_FOLDER / "using-packaged-src"

    shutil.rmtree(parent_output_using_project, ignore_errors=True)
    shutil.rmtree(parent_output_using_packaged_src, ignore_errors=True)

    contracts = ['xbulk']

    for contract in contracts:
        for package_whole_project_src in [True, False]:
            output_using_project = parent_output_using_project / contract / ("whole" if package_whole_project_src else "truncated")
            output_using_packaged_src = parent_output_using_packaged_src / contract / ("whole" if package_whole_project_src else "truncated")

            output_using_packaged_src.mkdir(parents=True, exist_ok=True)
            output_using_project.mkdir(parents=True, exist_ok=True)

            logging.info(f"Running docker for {contract} with package_whole_project_src={package_whole_project_src}")

            run_docker(
                project_path=project_path,
                package_whole_project_src=package_whole_project_src,
                packaged_src_path=None,
                contract_name=contract,
                image="sdk-rust-contract-builder:next",
                output_folder=output_using_project
            )

            logging.info("Checking output content...")
            output_using_project_files = sorted((output_using_project).rglob("*"))
            print(output_using_project_files)

            packaged_src_path = output_using_project / f"{contract}/{contract}-2.0.0.source.json"

            logging.info(f"Running docker for {contract} with package_whole_project_src={package_whole_project_src}, using packaged src={packaged_src_path}")

            logging.info("Checking src file...")

            content = packaged_src_path.read_text()
            print(content)

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

            for index, file in enumerate(using_project_output_files):
                if not file.is_file() or file.suffix == ".zip":
                    continue
                using_project_file_content = file.read_bytes()
                using_packaged_src_file_content = using_packaged_src_output_files[index].read_bytes()

                if using_project_file_content != using_packaged_src_file_content:
                    raise Exception(f"Files differ ({contract}): {file.name}")


if __name__ == "__main__":
    main(sys.argv[1:])
