
import shutil
from pathlib import Path

from multiversx_sdk_rust_contract_builder.main import main


def test_build_using_project_and_packaged_src():
    project_path = Path("./testdata/input/extracted/mx-exchange-sc")
    archive_path = Path("./testdata/input/archives/mx-exchange-sc-2.1.4-locked-token-wrapper.zip")
    cargo_target_dir = Path("/tmp/cargo-target-dir")
    output_using_project = Path("./testdata/output/using-project")
    output_using_packaged_src = Path("./testdata/output/using-packaged-src")

    shutil.rmtree(project_path, ignore_errors=True)
    shutil.unpack_archive(archive_path, project_path)

    contracts = ["pair", "farm", "router"]

    for contract in contracts:
        main(["--project", str(project_path), "--output", str(output_using_project), "--contract", contract, "--cargo-target-dir", str(cargo_target_dir)])
        code_hash_using_project = (output_using_project / f"{contract}/{contract}.codehash.txt").read_text().strip()

        packaged_src_path = output_using_project / f"{contract}/{contract}-0.0.0.source.json"

        main(["--packaged-src", str(packaged_src_path), "--output", str(output_using_packaged_src), "--contract", contract, "--cargo-target-dir", str(cargo_target_dir)])
        code_hash_using_packaged_src = (output_using_packaged_src / f"{contract}/{contract}.codehash.txt").read_text().strip()

        assert code_hash_using_project == code_hash_using_packaged_src
