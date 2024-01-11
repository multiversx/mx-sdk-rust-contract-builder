
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
        project_archive_url="https://github.com/multiversx/mx-exchange-sc/archive/refs/heads/reproducible-v2.1.1-staking-upgrade.zip",
        project_relative_path_in_archive="mx-exchange-sc-reproducible-v2.1.1-staking-upgrade",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "farm-staking": "6dc7c587b2cc4b177a192b709c092f3752b3dcf9ce1b484e69fe64dc333a9e0a",
            "farm": "931ca233826ff9dacd889967365db1cde9ed8402eb553de2a3b9d58b6ff1098d",
            "factory": "df06465b651594605466e817bfe9d8d7c68eef0f87df4a8d3266bcfb1bef6d83",
            "pair": "f3f08ebd758fada871c113c18017d9761f157d00b19c4d3beaba530e6c53afc2",
            "energy-factory": "241600c055df605cafd85b75d40b21316a6b35713485201b156d695b23c66a2f"
        },
        docker_image="multiversx/sdk-rust-contract-builder:v4.2.1"
    ),
    PreviousBuild(
        name="a.2",
        project_archive_url="https://github.com/multiversx/mx-metabonding-sc/archive/refs/heads/reproducible-v1.1.1.zip",
        project_relative_path_in_archive="mx-metabonding-sc-reproducible-v1.1.1",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "metabonding": "897b19e1990f7c487c99c12f50722febe1ee4468bcd3a7405641966dfff2791d"
        },
        docker_image="multiversx/sdk-rust-contract-builder:v4.2.1"
    ),
    PreviousBuild(
        name="a.3",
        project_archive_url="https://github.com/multiversx/mx-reproducible-contract-build-example-sc/archive/refs/tags/v0.4.7.zip",
        project_relative_path_in_archive="mx-reproducible-contract-build-example-sc-0.4.7",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "adder": "9fd12f88f9474ba115fb75e9d18a8fdbc4f42147de005445048442d49c3aa725",
            "multisig": "9600fc699c85fd5a24ecf28f0b8cf01dc281c81399fb018d5ad8405b7d401041",
            "multisig-full": "9eed9c35113209fc69631cf29aac6e81f0e331132bf6e46198e679259075ad49",
            "multisig-view": "3993cf3fb5cd18102e2b8946ea1997f6f1cc512537f453265ba1afd7378fc0c6",
            "lottery-esdt": "e06b1a5c7fb71181a79e9be6b86d8ad154e5c2def4da6d2f0aa5266163823291"
        },
        docker_image="multiversx/sdk-rust-contract-builder:v5.4.1"
    ),
    PreviousBuild(
        name="a.4",
        project_archive_url="https://github.com/multiversx/mx-contracts-rs/archive/refs/tags/v0.45.2.1-reproducible.zip",
        project_relative_path_in_archive="mx-contracts-rs-0.45.2.1-reproducible",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "adder": "384b680df7a95ebceca02ffb3e760a2fc288dea1b802685ef15df22ae88ba15b",
            "multisig": "b82f074c02e308b80cfb7144d7dc959bfac73e14dc3291837fdd8b042a7739cf",
            "multisig-full": "44a0eafb3bedfd671d1df586313f716924e2e4ef00ae7bf26df2c11eb4291389",
            "multisig-view": "d3e8328d525fcf196bb5bb4ce0741d9146dccb475461a693c407cdfa02334789",
            "lottery-esdt": "e06b1a5c7fb71181a79e9be6b86d8ad154e5c2def4da6d2f0aa5266163823291",
            "ping-pong-egld": "9283ca2f077edf2704053f0973fdd1eb90ee871ddcd672f962de4ba4422df84b"
        },
        docker_image="sdk-rust-contract-builder:next"
    ),
]
