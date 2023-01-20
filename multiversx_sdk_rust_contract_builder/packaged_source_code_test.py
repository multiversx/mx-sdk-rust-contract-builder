
from pathlib import Path

from multiversx_sdk_rust_contract_builder.packaged_source_code import \
    PackagedSourceCode

input_folder = Path("./testdata/input")
expected_folder = Path("./testdata/expected")
output_folder = Path("./testdata/output")


def test_packaged_source_code_from_filesystem():
    packaged_src = PackagedSourceCode.from_filesystem(input_folder / "hello", input_folder / "hello" / "foo")
    packaged_src.save_to_file(output_folder / "hello-foo-1.2.3.source.json")
    assert len(packaged_src.entries) == 7

    packaged_src = PackagedSourceCode.from_filesystem(input_folder / "hello", input_folder / "hello" / "bar")
    packaged_src.save_to_file(output_folder / "hello-bar-1.2.3.source.json")
    assert len(packaged_src.entries) == 4
