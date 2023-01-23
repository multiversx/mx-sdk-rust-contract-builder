
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
        project_archive_url="https://github.com/multiversx/mx-reproducible-contract-build-example-sc/archive/refs/tags/v0.1.5.zip",
        project_relative_path_in_archive=None,
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "adder": "58c6e78f40bd6ccc30d8a01f952b34a13ebfdad796a2526678be17c5d7820174"
        },
        docker_image="multiversx/sdk-rust-contract-builder:v4.0.3"
    ),
    PreviousBuild(
        name="a.2",
        project_archive_url="https://github.com/multiversx/mx-reproducible-contract-build-example-sc/archive/refs/tags/v0.1.5.zip",
        project_relative_path_in_archive=None,
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "adder": "58c6e78f40bd6ccc30d8a01f952b34a13ebfdad796a2526678be17c5d7820174"
        },
        docker_image="multiversx/sdk-rust-contract-builder:v4.0.3"
    ),
    PreviousBuild(
        name="a.3",
        project_archive_url="https://github.com/multiversx/mx-reproducible-contract-build-example-sc/archive/refs/tags/v0.1.5.zip",
        project_relative_path_in_archive=None,
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "adder": "58c6e78f40bd6ccc30d8a01f952b34a13ebfdad796a2526678be17c5d7820174"
        },
        docker_image="sdk-rust-contract-builder:next"
    ),
    PreviousBuild(
        name="b.1",
        project_archive_url="https://github.com/multiversx/mx-exchange-sc/archive/refs/tags/v1.5.4-metabonding-unbond.zip",
        project_relative_path_in_archive="mx-exchange-sc-1.5.4-metabonding-unbond",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "metabonding-staking": "4a9b2afa13eca738b1804c48b82a961afd67adcbbf2aa518052fa124ac060bea"
        },
        docker_image="multiversx/sdk-rust-contract-builder:v4.0.2"
    ),
    PreviousBuild(
        name="b.2",
        project_archive_url="https://github.com/multiversx/mx-exchange-sc/archive/refs/tags/v1.5.4-metabonding-unbond.zip",
        project_relative_path_in_archive="mx-exchange-sc-1.5.4-metabonding-unbond",
        packaged_src_url=None,
        contract_name="metabonding-staking",
        expected_code_hashes={
            "metabonding-staking": "4a9b2afa13eca738b1804c48b82a961afd67adcbbf2aa518052fa124ac060bea"
        },
        docker_image="multiversx/sdk-rust-contract-builder:v4.0.2"
    ),
    PreviousBuild(
        name="b.3",
        project_archive_url="https://github.com/multiversx/mx-exchange-sc/archive/refs/tags/v1.5.4-metabonding-unbond.zip",
        project_relative_path_in_archive="mx-exchange-sc-1.5.4-metabonding-unbond",
        packaged_src_url=None,
        contract_name="metabonding-staking",
        expected_code_hashes={
            "metabonding-staking": "4a9b2afa13eca738b1804c48b82a961afd67adcbbf2aa518052fa124ac060bea"
        },
        docker_image="multiversx/sdk-rust-contract-builder:v4.0.2"
    ),
    PreviousBuild(
        name="c.1",
        project_archive_url="https://github.com/multiversx/mx-exchange-sc/archive/refs/heads/reproducible-v2.1.1-staking-upgrade.zip",
        project_relative_path_in_archive="mx-exchange-sc-reproducible-v2.1.1-staking-upgrade",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "distribution": "17a30ad44291af84f6dbd84fdaf0a9a56ed7145d544c54fd74088bb544c4f98f",
            "energy-factory": "241600c055df605cafd85b75d40b21316a6b35713485201b156d695b23c66a2f",
            "energy-factory-mock": "83b2f26a52e3fe74953f2a8cfd81f169664a4e59dae4e5d5bb1d89956fd81d43",
            "energy-update": "8523bf84ac56626c70c31342487445bf8123e3ef5f906dcb39e8b5f16c4145b7",
            "factory": "df06465b651594605466e817bfe9d8d7c68eef0f87df4a8d3266bcfb1bef6d83",
            "farm": "931ca233826ff9dacd889967365db1cde9ed8402eb553de2a3b9d58b6ff1098d",
            "farm-staking": "6dc7c587b2cc4b177a192b709c092f3752b3dcf9ce1b484e69fe64dc333a9e0a",
            "farm-staking-proxy": "56468a6ae726693a71edcf96cf44673466dd980412388e1e4b073a0b4ee592d7",
            "farm-with-locked-rewards": "437b2a665e643b5885cf50ee865c467371ca6faa20a8ff14a4b626c775f49971",
            "fees-collector": "c46767232cd8551f8b0f4aa94dc419ddefc13eaaa5aa4b422749a300621149f3",
            "governance": "959388eadaf71ff106252c601ae2767a5c62d7bd0ab119381c28dc679975685e",
            "governance-v2": "786a6cf08f1d961814ebb062f149c9a943d39d7db93d8f53aa1fc42b8e652f49",
            "lkmex-transfer": "995311e0dbd75ddc51a5c0c71ab896245c996b9b3993d3118a153bfb5531e123",
            "locked-token-wrapper": "f9ee63d96163e3fac52a164c76d91c85fd77968393a50d4a96a7080e648d0a6c",
            "metabonding-staking": "f508c5643b3d5f5e79b68762a9ca9e247c753acd305a29009328c5ec5d153bdd",
            "pair": "f3f08ebd758fada871c113c18017d9761f157d00b19c4d3beaba530e6c53afc2",
            "pair-mock": "a54495375db964cf924391433605d602940174d4d28111b89b8689564d90e662",
            "pause-all": "2ad8aa911555b41e397541eb46cd1a7fa87186146f8c2b295e3916303833f3cd",
            "price-discovery": "6df095b15272b189c2e7b3628a21e17c1a6b26e5ed03e9a7bddac61be29d162f",
            "proxy-deployer": "5108e7419546872d235f0b7db5e01c5d04fec243bfa599c666629ead13bab0aa",
            "proxy_dex": "988dd8b632e1b4bb9b43e5636ef4c363dd4066186f64f6f783f9cd043aa906c1",
            "router": "c21ab56ef24b0719c101677170557e5aa61e1d17c1052ed7b2290cb26a5bdcd6",
            "simple-lock": "303290b7a08b091c29315dd6979c1f745fc05467467d7de64e252592074890a7",
            "simple-lock-whitelist": "c576c6106234e5f7978efb1885afe36c5d6da6a13c12b459fd7fe95967646d13",
            "token-unstake": "463e49892f64726450d0df5ab4ba26559ad882525ce5e93173a26fde8437266e",
        },
        docker_image="multiversx/sdk-rust-contract-builder:v4.0.2"
    ),
    PreviousBuild(
        name="c.2",
        project_archive_url="https://github.com/multiversx/mx-exchange-sc/archive/refs/heads/reproducible-v2.0-rc6.zip",
        project_relative_path_in_archive="mx-exchange-sc-reproducible-v2.0-rc6",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "distribution": "17a30ad44291af84f6dbd84fdaf0a9a56ed7145d544c54fd74088bb544c4f98f",
            "energy-factory": "62d60c8dec649614dd9cf04fb20b884c7658b12759fa14bf7e9c7be3880a5edd",
            "energy-factory-mock": "83b2f26a52e3fe74953f2a8cfd81f169664a4e59dae4e5d5bb1d89956fd81d43",
            "energy-update": "8523bf84ac56626c70c31342487445bf8123e3ef5f906dcb39e8b5f16c4145b7",
            "factory": "df06465b651594605466e817bfe9d8d7c68eef0f87df4a8d3266bcfb1bef6d83",
            "farm": "69f95b5f9a4d5b6bb101d5d2cf7495264a4d04de2b36653e0c8088cf6fad492a",
            "farm-staking": "ca0a8ceed8b8807b0fb078153c15167a3a235a61a76edc5023dfcacae0446125",
            "farm-staking-proxy": "56468a6ae726693a71edcf96cf44673466dd980412388e1e4b073a0b4ee592d7",
            "farm-with-locked-rewards": "c18d75ea788ece457788ad8849722a42dd4a12e6e23ab87f0cdffcc0116b61be",
            "fees-collector": "c46767232cd8551f8b0f4aa94dc419ddefc13eaaa5aa4b422749a300621149f3",
            "governance": "959388eadaf71ff106252c601ae2767a5c62d7bd0ab119381c28dc679975685e",
            "governance-v2": "786a6cf08f1d961814ebb062f149c9a943d39d7db93d8f53aa1fc42b8e652f49",
            "lkmex-transfer": "995311e0dbd75ddc51a5c0c71ab896245c996b9b3993d3118a153bfb5531e123",
            "locked-token-wrapper": "f9ee63d96163e3fac52a164c76d91c85fd77968393a50d4a96a7080e648d0a6c",
            "metabonding-staking": "f508c5643b3d5f5e79b68762a9ca9e247c753acd305a29009328c5ec5d153bdd",
            "pair": "23ce1e8910c105410b4a417153e4b38c550ab78b38b899ea786f0c78500caf21",
            "pair-mock": "a54495375db964cf924391433605d602940174d4d28111b89b8689564d90e662",
            "pause-all": "2ad8aa911555b41e397541eb46cd1a7fa87186146f8c2b295e3916303833f3cd",
            "price-discovery": "6df095b15272b189c2e7b3628a21e17c1a6b26e5ed03e9a7bddac61be29d162f",
            "proxy-deployer": "5108e7419546872d235f0b7db5e01c5d04fec243bfa599c666629ead13bab0aa",
            "proxy_dex": "988dd8b632e1b4bb9b43e5636ef4c363dd4066186f64f6f783f9cd043aa906c1",
            "router": "8429d332fb62b557b3549d3f509a55d6aff8638f53a5ee876358a831107102cf",
            "simple-lock": "303290b7a08b091c29315dd6979c1f745fc05467467d7de64e252592074890a7",
            "simple-lock-whitelist": "c576c6106234e5f7978efb1885afe36c5d6da6a13c12b459fd7fe95967646d13",
            "token-unstake": "463e49892f64726450d0df5ab4ba26559ad882525ce5e93173a26fde8437266e",
        },
        docker_image="multiversx/sdk-rust-contract-builder:v4.0.2"
    ),
    PreviousBuild(
        name="c.3",
        project_archive_url="https://github.com/multiversx/mx-exchange-sc/archive/refs/heads/reproducible-v2.1.3-price-discovery-comp-upgrade.zip",
        project_relative_path_in_archive="mx-exchange-sc-reproducible-v2.1.3-price-discovery-comp-upgrade",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "distribution": "c8f6a78ca4007608905484952c88b680afe450203ca89a9e176ff36472eb4e3c",
            "energy-factory": "1d444aaae54ab41c04ecf6147cfba16b03e5841382d69c65decb5fbd3bef6b25",
            "energy-factory-mock": "a55835cd6992f0c02331ee1b8a21b3163c0efc1a8c1c3fdb1b5e34944a358d66",
            "energy-update": "5ecde1bde66e1ccc10ac4bf8dcabfabf0d314ecaac51c72c3a19037256557885",
            "factory": "3bcee411030c9426500178f1e92b3a1d7c31a7ed2bbb29ab05d15a4eaac3a955",
            "farm": "4029cd4df87f2be4b7d1ed96161c9c3ab6fa44c090a574de4e6f1926ff302ea0",
            "farm-staking": "89833609549b085f258b8fac6272014d874918883cf5643b071fb097993cdf03",
            "farm-staking-proxy": "afe66cd648e293a98939af01a6b75180f0545ac3049ef26dfd6cfcdc7fcea51c",
            "farm-with-locked-rewards": "c1dcd37f29dbc5a810ef1893c07cd3d7af765cb5d7b0c7ac92f5a601df73e033",
            "fees-collector": "44a90c28bf35386cd533d22046243e02dc38cec00db948ef0c85392779c20593",
            "governance": "956d520e05e97327ce2b8d05872a758c0e88ddce15a298b3fb8b7e0cf4a5ef1c",
            "governance-v2": "995add2c509c29f4a8f875019f46831a0f5702fa21ea7a69e6fdad19bb6fda04",
            "lkmex-transfer": "1c776af3ec771aba18c1cb2bb567a583ed179d91c8765bfbdc2dd4ddcca65790",
            "locked-token-wrapper": "086a9baf3d89a54c2fccd066e36872d75406ac30ff1ed7c5ac9aae3a98b83284",
            "metabonding-staking": "c2c5bbed7f35767315c574dedbabdfbd5f18bf6cd2a561e3df08fc46637ef1a8",
            "pair": "c5c373155de76e6dfa040386947459d8cbdb4e7cc28d3dfe907922032a05e626",
            "pair-mock": "7a631dbc9e2ba07932c21d923292234110859d2ce5335851f0265aeaa37b7687",
            "pause-all": "2ad8aa911555b41e397541eb46cd1a7fa87186146f8c2b295e3916303833f3cd",
            "price-discovery": "96b51ec9df3eb7a8e72f297aac2c8e4e609e39ac5a5f6d861c0819d010b87fde",
            "proxy-deployer": "17e225e07b2ec759c86d70f6b61342f603135ac399b36bc48acab89f0bcfa483",
            "proxy_dex": "3cac5e915b9c8f8dfa711b1f4b1cf213380660cbd0afe3695cc73d4989abe301",
            "router": "5383bf12ad1ff9134782bd9aa9638bd16260ae7800434d01f853117e3db15c42",
            "simple-lock": "4f2747e6952b0e0aaa275e57dbd87afe63b1caf353ba25ff002b1a85185f3927",
            "simple-lock-whitelist": "3bc3cecbee78958e65efdaa077974d95d743d962254788d9280839362dc4da8b",
            "token-unstake": "2b0f59073bd697d75ec2009a3bf3c350b74ff9b10d6a7bfe1e13f653732ddb1a",
        },
        docker_image="multiversx/sdk-rust-contract-builder:v4.0.2"
    ),
    PreviousBuild(
        name="c.4",
        project_archive_url="https://github.com/multiversx/mx-exchange-sc/archive/refs/heads/reproducible-v2.1.4-locked-token-wrapper.zip",
        project_relative_path_in_archive="mx-exchange-sc-reproducible-v2.1.4-locked-token-wrapper",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "distribution": "51c9b6961443e67429ff6206fbb687427f8de739b50f02fb570269569e2c825d",
            "energy-factory": "04483a0014d8c633d3966b38a96f2ea85d462cdde84cc3f0ee9ed28932c392ec",
            "energy-factory-mock": "e5e95496bbfad534764eb67b3424ccae648353b39f89e41ba6874af6012a059f",
            "energy-update": "31fec2ec88c778bb7157519b8f5757ce3aefc8334c7c93834f5c4e1d667bf4b5",
            "factory": "91ef660172515fa6c5985f5cea06e96d9dfaae672e17a3cad6b2f4ad82ff2f0e",
            "farm": "b406b586b8124a6cb577b91cf970b5acdfee41bbe5e21b87201a27a2f9772fb7",
            "farm-staking": "7915b8e7c96f748afdd1a03a53d9c5377b1b11fcd59d4e6070094a5a0d7bff31",
            "farm-staking-proxy": "99ad18a0bb49ab45ee5a860ebab10dc964796fd0218752bca38b5666c916c0a2",
            "farm-with-locked-rewards": "a79baa1470a6b6232de6279417da046e753f7b9a4b9ae0e7e74f4f62da80a608",
            "fees-collector": "fb4f1f63a5bd33184afde0241cb69b9e9d172ed936263d688c65ab96a7fd2d0c",
            "governance": "e38189852ed794a6bd408c1147f90b4c47a9c6381c3a84b1b378ab6bfc9f74aa",
            "governance-v2": "192570f6866fd109371580f04a1ef7553a98c5603ebd1afd55a42f983c03df3c",
            "lkmex-transfer": "f850f9c7f70d3e198fa08e0d64538456b8e8ccdd6a5b8929f7faedd7cca85413",
            "locked-token-wrapper": "256d7144713e6875eacde2aaefdf222895bf024f4ab2ea4c7dfb02e60d1efba3",
            "metabonding-staking": "5cbcaaa8821db2a902477bce67a18a6f238f933863dded4c66bc5a5c9677dda7",
            "pair": "dfb32db0afeb85bdf7bcc02d823a818bf27ce217513ecf6c92f5ccb25425a191",
            "pair-mock": "a54495375db964cf924391433605d602940174d4d28111b89b8689564d90e662",
            "pause-all": "2ad8aa911555b41e397541eb46cd1a7fa87186146f8c2b295e3916303833f3cd",
            "price-discovery": "23deb3a6515a1a524fae6fb03613c042e2225d253da1e04532c66544167ac353",
            "proxy-deployer": "9224eb8803a2aba700ec24ad8447ebc55010cb0c200cc55042d9b97dadc0668b",
            "proxy_dex": "504f267a114cb46a6f3ba873dcfde43bd92d46fec61c830d45dfda2e368f52dc",
            "router": "0a1ce2edc277cd36098e0a44aab618ef30a048db60eb9c67bac251fb43b54aa6",
            "simple-lock": "74413279b467b72df4086efecfa0a773de284bfade1d9000106d13d47441daff",
            "simple-lock-whitelist": "b8f14e78635ad3894cb78f7d24302d17ee2059b353d1017e4b84f3beef2abc1a",
            "token-unstake": "3059ffec6f44259b8f2be56b9e1c67c72342f93c0c6f4b5cadc24364f2ee95e7",
        },
        docker_image="multiversx/sdk-rust-contract-builder:v4.0.2"
    ),
    PreviousBuild(
        name="c.5",
        project_archive_url="https://github.com/multiversx/mx-exchange-sc/archive/refs/heads/reproducible-v2.1.6-energy-factory-convert-for-scs.zip",
        project_relative_path_in_archive="mx-exchange-sc-reproducible-v2.1.6-energy-factory-convert-for-scs",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "energy-factory": "529fd987e7702b90044757073f36024d24cbe5cc8810d5abe93c6c5176a0ec53",
        },
        docker_image="multiversx/sdk-rust-contract-builder:v4.0.2"
    ),
    PreviousBuild(
        name="d.1",
        project_archive_url="https://github.com/multiversx/mx-nft-marketplace-sc/archive/refs/heads/reproducible-v2.0.1.zip",
        project_relative_path_in_archive="mx-nft-marketplace-sc-reproducible-v2.0.1",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "esdt-nft-marketplace": "aed8f014c914d2910cbb68b61adb757f8dbc8385842e717127482e1a66828bbe",
            "seller-contract-mock": "d3f42ae77ec60878ba62146a4209ef08a9400aecf083c96888ede316069985c0"
        },
        docker_image="multiversx/sdk-rust-contract-builder:v4.0.3"
    ),
    PreviousBuild(
        name="e.1",
        project_archive_url="https://github.com/multiversx/mx-metabonding-sc/archive/refs/heads/reproducible-v1.1.1.zip",
        project_relative_path_in_archive="mx-metabonding-sc-reproducible-v1.1.1",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "metabonding": "897b19e1990f7c487c99c12f50722febe1ee4468bcd3a7405641966dfff2791d"
        },
        docker_image="multiversx/sdk-rust-contract-builder:v4.0.2"
    )
]
