"""Pydantic loader using YAML serialization."""

import logging
from os import PathLike
from pathlib import Path
from typing import Union, Dict, Hashable, Any, Optional

import yaml
from pydantic import BaseSettings

import pydantic_loader
from pydantic_loader.encode import encode_pydantic_obj

_LOGGER = logging.getLogger(__name__)


def save_yaml(config: BaseSettings, config_file: Path):
    """Serialize the config class and save it as a yaml file."""
    dct = encode_pydantic_obj(config)
    try:
        val = yaml.dump(dct)
    except yaml.YAMLError as err:
        print(err)
        raise pydantic_loader.CfgError(err)

    config_file.parent.mkdir(exist_ok=True)
    with open(config_file, "w") as yaml_file:
        yaml_file.write(val)


def _load_yaml(
    config_file: Union[Path, PathLike]
) -> Union[Dict[Hashable, Any], list, None]:
    try:
        with open(config_file) as yaml_file:
            dct = yaml.load(yaml_file)
            return dct
    except yaml.YAMLError as err:
        raise pydantic_loader.CfgError(str(err))


def load_yaml(pydantic_obj, config_file: Optional[Path], on_error_return_default=False):
    """Load a config file and merge it into the config class.

    Args:
        pydantic_obj: A pydantic class to instantiate
        config_file: An optional config file location.
        on_error_return_default: If true loading is forgiving:
          On fail it will load default settings. Otherwise it will raise CfgError.


    Returns:
        A config instance

    raises:
        CfgError when loading fails and on_error_return_default is False.
    """
    return pydantic_loader.config.load_config(
        pydantic_obj,
        config_file,
        loader=_load_yaml,
        on_error_return_default=on_error_return_default,
    )
