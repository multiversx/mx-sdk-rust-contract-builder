
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
        project_archive_url="https://github.com/multiversx/mx-reproducible-contract-build-example-sc/archive/refs/tags/v0.4.0.zip",
        project_relative_path_in_archive="mx-reproducible-contract-build-example-sc-0.4.0",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "adder": "9fd12f88f9474ba115fb75e9d18a8fdbc4f42147de005445048442d49c3aa725",
            "multisig": "2101bc2a7a31ea42e5ffaadd86c1640009690e93b1cb46c3566ba5eac2984e36",
            "multisig-full": "ef468403354b6d3a728f86101354359fe6864187d216f674d99b31fc05313a39",
            "multisig-view": "3690af76be10c0520e3c3545cde8d9ef6a15c2d0af74dbd8704b4909644049c9"
        },
        docker_image="multiversx/sdk-rust-contract-builder:v5.1.0"
    ),
    PreviousBuild(
        name="a.2",
        project_archive_url="https://github.com/multiversx/mx-reproducible-contract-build-example-sc/archive/refs/tags/v0.4.3.zip",
        project_relative_path_in_archive="mx-reproducible-contract-build-example-sc-0.4.3",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "adder": "9fd12f88f9474ba115fb75e9d18a8fdbc4f42147de005445048442d49c3aa725",
            "multisig": "b73050629c11b1f1a20ca6232abcef07897624195691552e3f2e2fce47822166",
            "multisig-full": "37c3b90bdaa7d8d203385c91b0b5cb4d3c444ab9ec5263351978046a545854e3",
            "multisig-view": "ebaf987b041fcda297da71291d76736e4e98a1e449e5ec37908cdc0198e8be37"
        },
        docker_image="multiversx/sdk-rust-contract-builder:v5.3.0"
    ),
    PreviousBuild(
        name="a.3",
        project_archive_url="https://github.com/multiversx/mx-exchange-sc/archive/refs/heads/v2.4.1-pair-safe-price-v2-reproducible.zip",
        project_relative_path_in_archive="reproducible-v2.4.1-pair-safe-price-v2",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "pair": "e9f117971963cb3c24b14e2a7698d48c170335af2f5c8167774c48c3c1c654e3",
            "pair-full": "f1af2b2bb42a9f035745777e4b2d4f72478569224f204d0d0103801faff9663a",
            "safe-price-view": "b5a657445ae74423c60210c88a6fa89b0bd4bdd00d5f06e788e14495bccc34c9"
        },
        docker_image="sdk-rust-contract-builder:next"
    )
]
