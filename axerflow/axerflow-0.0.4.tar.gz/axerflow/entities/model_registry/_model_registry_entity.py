from abc import abstractmethod
from axerflow.entities._axerflow_object import _AxerflowObject


class _ModelRegistryEntity(_AxerflowObject):
    @classmethod
    @abstractmethod
    def from_proto(cls, proto):
        pass

    def __eq__(self, other):
        return dict(self) == dict(other)
