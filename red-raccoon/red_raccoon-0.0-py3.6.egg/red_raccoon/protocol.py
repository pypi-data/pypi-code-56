"""
This module contains helper functions for sending gRPC requests.
"""

import logging

from grpc import RpcError, StatusCode
from red_raccoon.exceptions import NotFound


logger = logging.getLogger(__name__)


def send_grpc_request(address, grpc_stub_function, msg):
    """
    Sends the provided Protobuf serialized message to the specified gRPC service using the provided
    gRPC stub function.

    :param address: the address to send the gRPC request to.
    :param grpc_stub_function: the stub to use when sending the gRPC request.
    :param msg: the message to send to the gRPC service.
    :return: the response.
    """
    try:
        response = grpc_stub_function(msg)
    except RpcError as exception:
        error_code = getattr(exception, "code")()
        if error_code == StatusCode.NOT_FOUND:
            raise NotFound(exception)

        logger.error(
            "Failed to communicate with gRPC service at: %s (%s: %s)",
            address, error_code.name, getattr(exception, "details")(),
        )
    else:
        logger.debug("Successfully sent %s bytes to gRPC service at: %s", msg.ByteSize(), address)
        return response
