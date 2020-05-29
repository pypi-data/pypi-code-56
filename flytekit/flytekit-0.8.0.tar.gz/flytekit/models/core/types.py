from __future__ import absolute_import

from flyteidl.core import types_pb2 as _types_pb2

from flytekit.models import common as _common


class BlobType(_common.FlyteIdlEntity):
    class BlobDimensionality(object):
        SINGLE = _types_pb2.BlobType.SINGLE
        MULTIPART = _types_pb2.BlobType.MULTIPART

    def __init__(self, format, dimensionality):
        """
        :param Text format: A string describing the format of the underlying blob data.
        :param int dimensionality: An integer from BlobType.BlobDimensionality enum
        """
        self._format = format
        self._dimensionality = dimensionality

    @property
    def format(self):
        """
        A string describing the format of the underlying blob data.
        :rtype: Text
        """
        return self._format

    @property
    def dimensionality(self):
        """
        An integer from BlobType.BlobDimensionality enum
        :rtype: int
        """
        return self._dimensionality

    def to_flyte_idl(self):
        """
        :rtype: flyteidl.core.types_pb2.BlobType
        """
        return _types_pb2.BlobType(
            format=self.format,
            dimensionality=self.dimensionality
        )

    @classmethod
    def from_flyte_idl(cls, proto):
        """
        :param flyteidl.core.types_pb2.BlobType proto:
        :rtype: BlobType
        """
        return cls(
            format=proto.format,
            dimensionality=proto.dimensionality
        )
