
from typing import Dict, List, Optional


class PreviousBuild:
    def __init__(self, name: str,
                 project_archive_url: Optional[str],
                 project_relative_path_in_archive: Optional[str],
                 packaged_src_url: Optional[str],
                 contract_name: Optional[str],
                 expected_code_hashes: Dict[str, str],
                 docker_image: str) -> None:
        self.name = name
        self.project_zip_url = project_archive_url
        self.project_relative_path_in_archive = project_relative_path_in_archive
        self.packaged_src_url = packaged_src_url
        self.contract_name = contract_name
        self.expected_code_hashs = expected_code_hashes
        self.docker_image = docker_image


previous_builds: List[PreviousBuild] = [
    PreviousBuild(
        name="a.1",
        project_archive_url="https://github.com/multiversx/mx-reproducible-contract-build-example-sc/archive/refs/tags/v0.4.6.zip",
        project_relative_path_in_archive="mx-reproducible-contract-build-example-sc-0.4.6",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "adder": "9fd12f88f9474ba115fb75e9d18a8fdbc4f42147de005445048442d49c3aa725",
            "multisig": "b73050629c11b1f1a20ca6232abcef07897624195691552e3f2e2fce47822166",
            "multisig-full": "37c3b90bdaa7d8d203385c91b0b5cb4d3c444ab9ec5263351978046a545854e3",
            "multisig-view": "ebaf987b041fcda297da71291d76736e4e98a1e449e5ec37908cdc0198e8be37",
            "lottery-esdt": "e06b1a5c7fb71181a79e9be6b86d8ad154e5c2def4da6d2f0aa5266163823291"
        },
        docker_image="multiversx/sdk-rust-contract-builder:v5.3.0"
    )
]
