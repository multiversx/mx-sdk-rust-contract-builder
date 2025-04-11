import os
from typing import Dict


class BuildMetadata:
    def __init__(
        self,
        version_rust: str,
        version_sc_meta: str,
        version_wasm_opt: str,
        target_platform: str,
    ):
        self.version_rust = version_rust
        self.version_sc_meta = version_sc_meta
        self.version_wasm_opt = version_wasm_opt
        self.target_platform = target_platform

    @classmethod
    def from_env(cls) -> 'BuildMetadata':
        return BuildMetadata(
            version_rust=os.environ["BUILD_METADATA_VERSION_RUST"],
            version_sc_meta=os.environ["BUILD_METADATA_VERSION_SC_META"],
            version_wasm_opt=os.environ["BUILD_METADATA_VERSION_WASM_OPT"],
            target_platform=os.environ["BUILD_METADATA_TARGETPLATFORM"],
        )

    def to_dict(self) -> Dict[str, str]:
        return {
            "versionRust": self.version_rust,
            "versionScTool": self.version_sc_meta,
            "versionWasmOpt": self.version_wasm_opt,
            "targetPlatform": self.target_platform,
        }
