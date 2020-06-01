from zealous.exceptions import BaseError


class RPCError(BaseError):
    message = "An unexpected RPCError occurred ({details})"


class RPCServerNotStarted(RPCError):
    message = "RPC server was not started"


class RPCServerAlreadyStarted(RPCError):
    message = "RPC server was already started"


class RPCServerInvalidConfig(RPCError):
    message = "RPC server configuration is invalid ({reason})"


class RPCServerInterfaceNotImplemented(RPCError):
    message = (
        "RPC server interface {interface} for resource {resource} not implemented."
    )

    def __init__(self, *, resource: str, interface: str) -> None:
        super().__init__(resource=resource, interface=interface)
        self.resource = resource
        self.interface = interface


class RPCRemoteError(RPCError):
    """An error raised in RPC backend and re-raised by the client."""

    message = "A remote exception occurred ({exc_type}: {exc_message})"

    def __init__(self, *, exc_type: str, exc_message: str) -> None:
        super().__init__(exc_type=exc_type, exc_message=exc_message)
        self.exc_type = exc_type
        self.exc_message = exc_message
