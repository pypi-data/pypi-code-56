import time
from os import path
from typing import List

from pyterum.logger import logger
from pyterum import env

# Interval in seconds before retrying
RETRY_INTERVAL = 5

# Wait until a requested file becomes available on disk, then return the path to it
# retries <0 means infinite retries
def _await_file(name:str, retries:int=-1) -> str:
    # validate existence of passed name
    if "config_files" not in env._CONFIG_DATA.keys():
        logger.fatal(f"No config files were passed to this process, cannot get filepath")
    if name not in env._CONFIG_DATA["config_files"].keys():
        logger.fatal(f"'{name}' is not included in this process' config files. Valid names are '{env._CONFIG_DATA['config_files'].keys()}'")
    
    file_path = path.join(env.CONFIG_PATH, env._CONFIG_DATA["config_files"][name])
    existent = path.exists(file_path)
    while not existent and abs(retries) != 0:
        logger.info(f"Config file '{file_path}' not yet available, retrying...")
        time.sleep(RETRY_INTERVAL)
        existent = path.exists(file_path)
        retries -= 1 if retries > 0 else 0

    if existent:
        return file_path

    raise Exception(f"PathError: Cannot retrieve config file '{name}'")


# Get path to a single config file when it becomes available
def get_filepath(name:str, retries:int=-1) -> str:
    assert(env.CONFIG_PATH != "" and path.exists(env.CONFIG_PATH))
    return _await_file(name, retries=retries)

# Get paths to multiple config files when they become available
def get_filepaths(names:List[str], retries:int=-1) -> List[str]:
    assert(env.CONFIG_PATH != "" and path.exists(env.CONFIG_PATH))
    paths = []
    for name in names:
        paths.append(_await_file(name, retries=retries))
    return paths

# Get one value from the JSON structure inserted into the ITERUM_CONFIG env variable
def get(key:str):
    env.verify_shared_envs()
    if key in env._CONFIG_DATA:
        return env._CONFIG_DATA[key]
    else:
        logger.warn(f"'{key}' is not a field in the received iterum config, valid keys are '{env._CONFIG_DATA.keys()}'")
        return None