from axerflow.entities._axerflow_object import _AxerflowObject
from axerflow.entities.run_data import RunData
from axerflow.entities.run_info import RunInfo
from axerflow.exceptions import AxerflowException
from axerflow.protos.service_pb2 import Run as ProtoRun


class Run(_AxerflowObject):
    """
    Run object.
    """

    def __init__(self, run_info, run_data):
        if run_info is None:
            raise AxerflowException("run_info cannot be None")
        self._info = run_info
        self._data = run_data

    @property
    def info(self):
        """
        The run metadata, such as the run id, start time, and status.

        :rtype: :py:class:`axerflow.entities.RunInfo`
        """
        return self._info

    @property
    def data(self):
        """
        The run data, including metrics, parameters, and tags.

        :rtype: :py:class:`axerflow.entities.RunData`
        """
        return self._data

    def to_proto(self):
        run = ProtoRun()
        run.info.MergeFrom(self.info.to_proto())
        if self.data:
            run.data.MergeFrom(self.data.to_proto())
        return run

    @classmethod
    def from_proto(cls, proto):
        return cls(RunInfo.from_proto(proto.info), RunData.from_proto(proto.data))

    def to_dictionary(self):
        run_dict = {
            "info": dict(self.info),
        }
        if self.data:
            run_dict["data"] = self.data.to_dictionary()
        return run_dict
