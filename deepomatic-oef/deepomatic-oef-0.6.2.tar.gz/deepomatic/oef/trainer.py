from deepomatic.oef.utils import serializer
from deepomatic.oef.protos import trainer_pb2


class Trainer(serializer.Serializer):
    """A trainer object"""

    optional_fields = ['update_trainable_variables', 'freeze_variables', 'do_not_restore_variables']


serializer.register_all(__name__, trainer_pb2)
