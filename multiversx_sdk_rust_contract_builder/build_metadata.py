import os
from typing import Dict


class BuildMetadata:
    def __init__(
        self,
        builder_name: str,
        target_platform: str,
    ):
        self.builder_name = builder_name
        self.target_platform = target_platform

    @classmethod
    def from_env(cls) -> 'BuildMetadata':
        return BuildMetadata(
            builder_name=os.environ["BUILD_METADATA_BUILDER_NAME"],
            target_platform=os.environ["BUILD_METADATA_TARGETPLATFORM"],
        )

    def to_dict(self) -> Dict[str, str]:
        return {
            "builderName": self.builder_name,
            "targetPlatform": self.target_platform,
        }
