
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
        project_archive_url="https://github.com/multiversx/mx-reproducible-contract-build-example-sc/archive/refs/tags/v0.3.0-alpha.1.zip",
        project_relative_path_in_archive=None,
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "adder": "9fd12f88f9474ba115fb75e9d18a8fdbc4f42147de005445048442d49c3aa725"
        },
        docker_image="sdk-rust-contract-builder:next"
    )
]
