"""
The ``axerflow.models`` module provides an API for saving machine learning models in
"flavors" that can be understood by different downstream tools.

The built-in flavors are:

- :py:mod:`axerflow.pyfunc`
- :py:mod:`axerflow.h2o`
- :py:mod:`axerflow.keras`
- :py:mod:`axerflow.pytorch`
- :py:mod:`axerflow.sklearn`
- :py:mod:`axerflow.spark`
- :py:mod:`axerflow.tensorflow`
- :py:mod:`axerflow.xgboost`

For details, see `Axerflow Models <../models.html>`_.
"""

from .model import Model
from .flavor_backend import FlavorBackend
from .signature import ModelSignature, infer_signature
from .utils import ModelInputExample

__all__ = ["Model", "ModelSignature", "infer_signature", "FlavorBackend"]
