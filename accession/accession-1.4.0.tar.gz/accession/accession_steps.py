import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from encode_utils.connection import Connection


class AccessionStep:
    """
    Model of a step performed during accessioning. Corresponds to a single step in the
    accession steps json's accession.steps array.
    """

    def __init__(self, step_params: Dict[str, Any]):
        self.step_run: str = step_params["dcc_step_run"]
        self.step_version: str = step_params["dcc_step_version"]
        self.wdl_task_name: str = step_params["wdl_task_name"]
        self.requires_replication: bool = step_params.get("requires_replication", False)
        self.wdl_files: List[FileParams] = [
            FileParams(i) for i in step_params["wdl_files"]
        ]

    def get_portal_step_run(self, aliases: List[str]) -> Dict[str, Any]:
        """
        Get the portal's dict representation of the step run with special profile key to
        enable posting with encode_utils.
        """
        payload = {
            "aliases": aliases,
            "status": "in progress",
            "analysis_step_version": self.step_version,
            Connection.PROFILE_KEY: "analysis_step_runs",
        }
        return payload


class AccessionSteps:
    def __init__(self, path_to_accession_step_json: Union[str, Path]):
        self.path = path_to_accession_step_json
        self._steps: Optional[Dict[str, Any]] = None
        self._content: Optional[List] = None

    @property
    def steps(self) -> Dict[str, Any]:
        """
        Corresponds to the entire accession steps JSON, not just the accession.steps
        """
        if self._steps is None:
            with open(self.path) as fp:
                self._steps = json.load(fp)
        return self._steps

    @property
    def content(self) -> List[AccessionStep]:
        if self._content is None:
            new_content = []
            for step in self.steps["accession.steps"]:
                new_content.append(AccessionStep(step))
            self._content = new_content
        return self._content

    @property
    def raw_fastqs_keys(self) -> Optional[str]:
        return self.steps.get("raw_fastqs_keys")


class DerivedFromFile:
    def __init__(self, derived_from_file: Dict[str, Any]):
        self.allow_empty: bool = derived_from_file.get("allow_empty", False)
        self.derived_from_filekey: str = derived_from_file["derived_from_filekey"]
        self.derived_from_inputs: bool = derived_from_file.get(
            "derived_from_inputs", False
        )
        self.derived_from_task: str = derived_from_file["derived_from_task"]
        self.derived_from_output_type: Optional[str] = derived_from_file.get(
            "derived_from_output_type"
        )
        self.disallow_tasks: List[str] = derived_from_file.get("disallow_tasks", [])


class FileParams:
    """
    Represents the spec for the file to accession as defined in the template
    """

    def __init__(self, file_params: Dict[str, Any]):
        self.filekey: str = file_params["filekey"]
        self.file_format: str = file_params["file_format"]
        self.output_type: str = file_params["output_type"]
        self.derived_from_files: List[DerivedFromFile] = [
            DerivedFromFile(i) for i in file_params["derived_from_files"]
        ]
        self.file_format_type: Optional[str] = file_params.get("file_format_type")
        self.callbacks: List[str] = file_params.get("callbacks", [])
        self.quality_metrics: List[str] = file_params.get("quality_metrics", [])
