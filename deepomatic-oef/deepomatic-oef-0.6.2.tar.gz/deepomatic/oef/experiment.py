from deepomatic.oef.utils import serializer
from deepomatic.oef.protos import experiment_pb2


serializer.register_all(__name__, experiment_pb2)
