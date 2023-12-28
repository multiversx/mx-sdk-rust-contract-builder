
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
        project_archive_url="https://github.com/multiversx/mx-exchange-sc/archive/refs/heads/reproducible-v2.4.1-pair-safe-price-v2.zip",
        project_relative_path_in_archive="mx-exchange-sc-reproducible-v2.4.1-pair-safe-price-v2",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "pair": "e9f117971963cb3c24b14e2a7698d48c170335af2f5c8167774c48c3c1c654e3",
            "pair-full": "f1af2b2bb42a9f035745777e4b2d4f72478569224f204d0d0103801faff9663a",
            "safe-price-view": "b5a657445ae74423c60210c88a6fa89b0bd4bdd00d5f06e788e14495bccc34c9"
        },
        docker_image="sdk-rust-contract-builder:next"
    ),
    PreviousBuild(
        name="a.4",
        project_archive_url="https://github.com/multiversx/mx-exchange-sc/archive/refs/heads/reproducible-v2.5.2-governance-merkle-tree.zip",
        project_relative_path_in_archive="mx-exchange-sc-reproducible-v2.5.2-governance-merkle-tree",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "lkmex-transfer": "49809df9f07839f965f8197721083cf403c3db969ddc47b5940b4ee8b464af92",
            "router": "3257d57945736298c96aa23f99ea0fba3b6da01f9d2103d81230d05cff62cb5a",
            "pair": "e9f117971963cb3c24b14e2a7698d48c170335af2f5c8167774c48c3c1c654e3",
            "locked-token-wrapper": "1d317cfa2bbe22ea1f878f8a32f90712d49f68a01665b86657d36910b430522f",
            "safe-price-view": "b5a657445ae74423c60210c88a6fa89b0bd4bdd00d5f06e788e14495bccc34c9"
        },
        docker_image="sdk-rust-contract-builder:next"
    ),
    PreviousBuild(
        name="a.5",
        project_archive_url="https://github.com/multiversx/mx-exchange-sc/archive/refs/heads/reproducible-v1.10.4-backwards-comp-proxy-dex.zip",
        project_relative_path_in_archive="mx-exchange-sc-reproducible-v1.10.4-backwards-comp-proxy-dex",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "farm-staking-proxy": "ee61abb8e639df4696900c5efdac6bec747679c149be26476ee7e384e35b1ff2",
            "proxy_dex": "8bab3716a1a92bad1b5cb77b97a09cce1ffabd56b954d881b93e1b480984c3d2",
            "factory": "b75f481df42c076f51cd7af04b914bc581e51784b31136ae27db368b37bd87b1",
            "farm_with_lock": "6b9d9a0f6bba6004c7c1163890ea0794cc61ab16c967e1c5c2cd2b8a7c19ebbf",
        },
        docker_image="sdk-rust-contract-builder:next"
    ),
    PreviousBuild(
        name="a.6",
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
        docker_image="sdk-rust-contract-builder:next"
    ),
    PreviousBuild(
        name="a.7",
        project_archive_url="https://github.com/multiversx/mx-exchange-sc/archive/refs/heads/reproducible-v2.0-rc6-reproducible.zip",
        project_relative_path_in_archive="mx-exchange-sc-reproducible-v2.0-rc6-reproducible",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "pair": "23ce1e8910c105410b4a417153e4b38c550ab78b38b899ea786f0c78500caf21",
            "simple-lock": "303290b7a08b091c29315dd6979c1f745fc05467467d7de64e252592074890a7",
            "farm-staking-proxy": "56468a6ae726693a71edcf96cf44673466dd980412388e1e4b073a0b4ee592d7"
        },
        docker_image="sdk-rust-contract-builder:next"
    ),
    PreviousBuild(
        name="a.8",
        project_archive_url="https://github.com/multiversx/mx-exchange-sc/archive/refs/heads/reproducible-v1.10.2-legacy-farm-stripdown.zip",
        project_relative_path_in_archive="mx-exchange-sc-reproducible-v1.10.2-legacy-farm-stripdown",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "farm": "bac43c58b865f55f303ae2d4100c5fe2d4492bc50cfb131d8206200039808242"
        },
        docker_image="sdk-rust-contract-builder:next"
    )
]
