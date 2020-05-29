from __future__ import absolute_import
from flytekit.models import common as _common
from flyteidl.core import errors_pb2 as _errors_pb2


class ContainerError(_common.FlyteIdlEntity):

    class Kind(object):
        NON_RECOVERABLE = _errors_pb2.ContainerError.NON_RECOVERABLE
        RECOVERABLE = _errors_pb2.ContainerError.RECOVERABLE

    def __init__(self, code, message, kind):
        """
        :param Text code: A succinct code about the error
        :param Text message: Whatever message you want to surface about the error
        :param int kind: A value from the ContainerError.Kind enum.
        """
        self._code = code
        self._message = message
        self._kind = kind

    @property
    def code(self):
        """
        :rtype: Text
        """
        return self._code

    @property
    def message(self):
        """
        :rtype: Text
        """
        return self._message

    @property
    def kind(self):
        """
        :rtype: int
        """
        return self._kind

    def to_flyte_idl(self):
        """
        :rtype: flyteidl.core.errors_pb2.ContainerError
        """
        return _errors_pb2.ContainerError(code=self.code, message=self.message, kind=self.kind)

    @classmethod
    def from_flyte_idl(cls, proto):
        """
        :param flyteidl.core.errors_pb2.ContainerError proto:
        :rtype: ContainerError
        """
        return cls(proto.code, proto.message, proto.kind)


class ErrorDocument(_common.FlyteIdlEntity):

    def __init__(self, error):
        """
        :param ContainerError error:
        """
        self._error = error

    @property
    def error(self):
        """
        :rtype: ContainerError
        """
        return self._error

    def to_flyte_idl(self):
        """
        :rtype: flyteidl.core.errors_pb2.ErrorDocument
        """
        return _errors_pb2.ErrorDocument(error=self.error.to_flyte_idl())

    @classmethod
    def from_flyte_idl(cls, proto):
        """
        :param flyteidl.core.errors_pb2.ErrorDocument proto:
        :rtype: ErrorDocument
        """
        return cls(ContainerError.from_flyte_idl(proto.error))
