from __future__ import annotations

from typing import Tuple
from typing import TypeVar
from typing import Union

from .schema import Schema


# General purpose TypeVars
T = TypeVar("T")
CoT = TypeVar("CoT", covariant=True)
ContraT = TypeVar("ContraT", contravariant=True)
ClsT = TypeVar("ClsT")
SelfT = TypeVar("SelfT")

# Schema TypeVars
_SchemaInT_bound = Schema
SchemaInT = TypeVar("SchemaInT", bound=_SchemaInT_bound)
SchemaInCoT = TypeVar("SchemaInCoT", bound=_SchemaInT_bound, covariant=True)
SchemaInContraT = TypeVar("SchemaInContraT", bound=_SchemaInT_bound, contravariant=True)

_SchemaOutT_bound = Union[Schema, Schema, Tuple[Schema, ...], None]
SchemaOutT = TypeVar("SchemaOutT", bound=_SchemaOutT_bound)
SchemaOutCoT = TypeVar("SchemaOutCoT", bound=_SchemaOutT_bound, covariant=True)
SchemaOutContraT = TypeVar(
    "SchemaOutContraT", bound=_SchemaOutT_bound, contravariant=True
)
