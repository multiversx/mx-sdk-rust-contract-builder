import shutil
import sys
from typing import List

from integration_tests.config import PARENT_OUTPUT_FOLDER
from integration_tests.shared import download_project_repository, run_docker
from multiversx_sdk_rust_contract_builder.main import main


def main(cli_args: List[str]):
    project_path = download_project_repository("https://github.com/multiversx/mx-exchange-sc/archive/refs/heads/main.zip", "mx-exchange-sc-main")
    output_using_project = PARENT_OUTPUT_FOLDER / "using-project"
    output_using_packaged_src = PARENT_OUTPUT_FOLDER / "using-packaged-src"

    shutil.rmtree(output_using_project, ignore_errors=True)
    shutil.rmtree(output_using_packaged_src, ignore_errors=True)

    output_using_project.mkdir(parents=True)
    output_using_packaged_src.mkdir(parents=True)

    contracts = ['distribution', 'energy-factory', 'energy-update', 'factory', 'farm', 'farm-staking', 'farm-staking-proxy', 'farm-with-locked-rewards', 'fees-collector', 'governance', 'governance-v2', 'lkmex-transfer', 'locked-token-wrapper', 'metabonding-staking', 'pair', 'pause-all', 'price-discovery', 'proxy-deployer', 'proxy_dex', 'router', 'simple-lock', 'simple-lock-whitelist', 'token-unstake']

    for contract in contracts:
        run_docker(
            project_path=project_path,
            packaged_src_path=None,
            contract_name=contract,
            image="sdk-rust-contract-builder:next",
            output_folder=output_using_project
        )

        packaged_src_path = output_using_project / f"{contract}/{contract}-0.0.0.source.json"

        run_docker(
            project_path=None,
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
