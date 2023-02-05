
from pathlib import Path
from typing import Any, Dict


class BuildOptions:
    def __init__(
        self,
        project_folder: Path,
        parent_output_folder: Path,
        package_whole_project_src: bool,
        specific_contract: str,
        cargo_target_dir: Path,
        no_wasm_opt: bool,
        context: str,
        build_root_folder: Path,
    ) -> None:
        self.project_folder = project_folder
        self.parent_output_folder = parent_output_folder
        self.package_whole_project_src = package_whole_project_src
        self.specific_contract = specific_contract
        self.cargo_target_dir = cargo_target_dir
        self.no_wasm_opt = no_wasm_opt
        self.context = context
        self.build_root_folder = build_root_folder

    def to_dict(self) -> Dict[str, Any]:
        return {
            "projectFolder": str(self.project_folder),
            "parentOutputFolder": str(self.parent_output_folder),
            "packageWholeProjectSrc": self.package_whole_project_src,
            "specificContract": self.specific_contract,
            "cargoTargetDir": str(self.cargo_target_dir),
            "noWasmOpt": self.no_wasm_opt,
            "context": self.context,
            "buildRootFolder": str(self.build_root_folder),
        }
