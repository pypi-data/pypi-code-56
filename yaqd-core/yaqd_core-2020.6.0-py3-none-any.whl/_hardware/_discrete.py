#! /usr/bin/env python3
import pathlib
from typing import Dict, Any, Sequence, Tuple, Union, Optional

from ._base import Hardware

__all__ = ["DiscreteHardware"]


class DiscreteHardware(Hardware):
    traits = ["is-discrete"]
    _kind: str = "discrete-hardware"
    _version: Optional[str] = None  # this class should not be directly instantiated

    def __init__(
        self, name: str, config: Dict[str, Any], config_filepath: pathlib.Path
    ):
        self._position_identifiers: Dict[str, Any] = config.get("identifiers", {})
        self._position_identifier = None
        super().__init__(name, config, config_filepath)

    def get_state(self):
        state = super().get_state()
        if self._position_identifier is not None:
            state["position_identifier"] = self._position_identifier
        return state

    def get_position_identifiers(self):
        return self._position_identifiers

    def set_identifier(self, identifier):
        p = self._position_identifiers[identifier]
        self.set_position(p)

    def get_identifier(self):
        return self._position_identifier
