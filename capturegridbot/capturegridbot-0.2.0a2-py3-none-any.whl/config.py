import os

import toml


class Config:
    def __init__(self, path: str):
        self._cfg = {}
        self._path = str(path)
        self._dirty = False

        if os.path.exists(path):
            with open(path, 'r') as input_file:
                self._cfg = toml.load(input_file)

    def save(self):
        if self._dirty:
            with open(self._path, 'w') as output_file:
                toml.dump(self._cfg, output_file)

    @property
    def capture_grid_path(self):
        return self._cfg.get('capture_grid_path', '/snap/bin/capturegrid4')

    @property
    def override_destination(self):
        return self._cfg.get('override_destination')

    @property
    def output_folder_name(self):
        return self._cfg.get('output_folder_name', 'capturegridbot')
