from typing import Optional, List
from pkg_resources import resource_filename
from random import choice, sample


def _get_path_to_name_file(name: str) -> str:
    return resource_filename('randword', 'data/names/') + f'{name}.txt'


def get_random_name():
    pass
