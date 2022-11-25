from pathlib import Path

from build_contract_rust import builder


def test_build_project():
    outcome = builder.build_project(
        project_path=Path("./testdata/adder"),
        parent_output_directory=Path("./testdata/output"),
        specific_contract=None,
        cargo_target_dir=Path("/tmp/cargo-target-dir"),
        no_wasm_opt=False
    )

    assert outcome.get_version("adder") == "1.2.3"
    assert outcome.get_codehash("adder") == "58c6e78f40bd6ccc30d8a01f952b34a13ebfdad796a2526678be17c5d7820174"
