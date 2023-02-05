import os
from typing import Dict


class BuildMetadata:
    def __init__(self, builder_name: str, version_rust: str, version_binaryen: str):
        self.builder_name = builder_name
        self.version_rust = version_rust
        self.version_binaryen = version_binaryen

    @classmethod
    def from_env(cls) -> 'BuildMetadata':
        return BuildMetadata(
            builder_name=os.environ["BUILD_METADATA_BUILDER_NAME"],
            version_rust=os.environ["BUILD_METADATA_VERSION_RUST"],
            version_binaryen=os.environ["BUILD_METADATA_VERSION_BINARYEN"],
        )

    def to_dict(self) -> Dict[str, str]:
        return {
            "builderName": self.builder_name,
            "versionRust": self.version_rust,
            "versionBinaryen": self.version_binaryen,
        }
