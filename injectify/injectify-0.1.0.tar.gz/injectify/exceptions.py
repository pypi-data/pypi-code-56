"""
injectify.exceptions
~~~~~~~~~~~~~~~~~

This module contains exceptions that power Injectify.
"""


class InjectException(Exception):
    """There was an ambigious exception that occured."""


class ArgumentError(InjectException, ValueError):
    """Raised when an invalid or conflicting function argument is supplied."""
