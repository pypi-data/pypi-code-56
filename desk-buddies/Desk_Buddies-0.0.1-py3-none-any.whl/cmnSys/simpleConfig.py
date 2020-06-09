import errno
import json
import os
from collections import UserDict

from cmnUtils.safeOpen import safe_open_w


class SimpleConfig(UserDict):

    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.set_default_data()
        try:
            with open(json_file_path) as json_file:
                client_set = json.load(json_file)
                for (key, val) in client_set.items():
                    self.data[key] = val
        except FileNotFoundError:
            pass

    def write(self):
        with safe_open_w(self.json_file_path) as file:
            json.dump(self.data, file)

    def set_default_data(self):
        pass
