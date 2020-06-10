import os
from typing import Optional

import toml


class Config:
    def __init__(self, path: str):
        self._cfg = {}
        self._path = str(path)

        if os.path.exists(path):
            with open(path, 'r') as input_file:
                self._cfg = toml.load(input_file)

    @property
    def capture_grid_path(self) -> str:
        return str(self._cfg.get('capture_grid_path', '/snap/bin/capturegrid4'))

    @property
    def override_destination(self) -> Optional[str]:
        return self._cfg.get('override_destination')

    @property
    def output_folder_name(self) -> str:
        return str(self._cfg.get('output_folder_name', 'capturegridbot'))

    @property
    def filename_expression(self) -> str:
        return str(self._cfg.get('filename_expression', '[c]_[d]_[b4]'))

    @property
    def auto_connect(self) -> bool:
        return bool(self._cfg.get('check_for_updates', True))

    @property
    def auto_synchronise_time(self) -> bool:
        return bool(self._cfg.get('check_for_updates', True))
