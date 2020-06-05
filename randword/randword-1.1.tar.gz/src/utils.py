from os import path
from distutils.sysconfig import get_python_lib


def get_path_to_pos_file(part_of_speech: str) -> str:
    if path.isfile(get_python_lib() + '/plateDetect'):
        package_path = get_python_lib() + '/plateDetect'
    else:
        package_path = path.dirname(__file__)

    return f'{package_path}/words/{part_of_speech}.txt'
