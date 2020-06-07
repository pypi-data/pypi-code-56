"""
The ``axerflow.tracking`` module provides a Python CRUD interface to Axerflow experiments
and runs. This is a lower level API that directly translates to Axerflow
`REST API <../rest-api.html>`_ calls.
For a higher level API for managing an "active run", use the :py:mod:`axerflow` module.
"""

from axerflow.tracking.client import AxerflowClient
from axerflow.tracking._tracking_service.utils import (
    set_tracking_uri,
    get_tracking_uri,
    is_tracking_uri_set,
    _get_store,
    _TRACKING_URI_ENV_VAR
)
from axerflow.tracking.fluent import _EXPERIMENT_ID_ENV_VAR, _EXPERIMENT_NAME_ENV_VAR, \
    _RUN_ID_ENV_VAR

__all__ = [
    "AxerflowClient",
    "get_tracking_uri",
    "set_tracking_uri",
    "is_tracking_uri_set",
    "_get_store",
    "_EXPERIMENT_ID_ENV_VAR",
    "_RUN_ID_ENV_VAR",
    "_TRACKING_URI_ENV_VAR",
]
