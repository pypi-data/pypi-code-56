"""
This module contains custom exceptions within the context of the Red Raccoon project.
"""


class NotFound(Exception):
    """
    The following exception should be raised if an object could not be found (e.g. in response to
    a gRPC request).
    """
