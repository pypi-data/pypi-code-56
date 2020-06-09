from deepomatic.oef.utils import serializer
from deepomatic.oef.protos.models.image.utils import hyperparameters_pb2

serializer.register_all(__name__, hyperparameters_pb2)
