
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
        docker_image="multiversx/sdk-rust-contract-builder:v5.4.1"
    ),
    PreviousBuild(
        name="a.2",
        project_archive_url="https://github.com/multiversx/mx-contracts-rs/archive/refs/tags/v0.45.2.1-reproducible.zip",
        project_relative_path_in_archive="mx-contracts-rs-0.45.2.1-reproducible",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "adder": "384b680df7a95ebceca02ffb3e760a2fc288dea1b802685ef15df22ae88ba15b",
            "multisig": "87cb62542c9b2d0b5a791cb35f7e44e71bb6d768d6ddb93155be61ad76267475",
            "multisig-full": "f6b5457682b39ea1bd52fd6fe293257a3d5a5bb931c9e404c9ba24617cd51438",
            "multisig-view": "1904fe0bfd12cb90fda87e5cf2d2f211d9eed8b48c296e6d858547bfe39bec0c",
            "lottery-esdt": "a54bd4278b12cc93fedd6ca0addf6aad4043528c33e54ce43cf92d4d2dd755ee",
            "ping-pong-egld": "8b107da10aef0d9610a939c4ca07c666674c465d0266fb28d5f981861f084f62"
        },
        docker_image="multiversx/sdk-rust-contract-builder:v6.1.2"
    ),
    PreviousBuild(
        name="a.3",
        project_archive_url="https://github.com/multiversx/mx-sovereign-sc/archive/e9a4f1fc8d963d48cbce0fb0cf673621cc0832ac.zip",
        project_relative_path_in_archive="mx-sovereign-sc-e9a4f1fc8d963d48cbce0fb0cf673621cc0832ac",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "sov-esdt-safe": "adc4e4f69b15153919c0bcf88df6436d4fcfacbc2da6a39e6bcc3f30927c80ad",
            "fee-market": "0b81078e61efd692ebb3f83b437da9cf83ffff7843aeb0a66a71b5ddff3b2fb2"
        },
        docker_image="sdk-rust-contract-builder:next"
    ),
]
