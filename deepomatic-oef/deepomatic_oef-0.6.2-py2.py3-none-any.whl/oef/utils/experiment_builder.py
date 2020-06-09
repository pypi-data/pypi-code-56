from google.protobuf.descriptor import FieldDescriptor

from deepomatic.oef.configs import model_list
from deepomatic.oef.utils import class_helpers
from deepomatic.oef.utils.serializer import Serializer
from deepomatic.oef.protos.experiment_pb2 import Experiment
import logging

logger = logging.getLogger(__name__)


class InvalidNet(Exception):
    pass


class ExperimentBuilder(object):
    """
    This class can build a Experiment protobuf given the pre-determined parameters. You can also pass
    additionnal parameters to override the default arguments. In that purpose, all fields of Model and its
    sub-messages are assumed to have a different name (this assumpition is checked by model_generator).
    """

    _model_list = None

    def __init__(self, model_type_key):
        if self._model_list is None:
            self.load_model_list()
        if model_type_key not in self._model_list:
            # Try model_type_key reordering to provide backward compatibility with oef<0.5.0
            model_type_key_parts = model_type_key.split('.')
            model_type_key_new_format = '.'.join([model_type_key_parts[0], model_type_key_parts[-1]] + model_type_key_parts[1:-1])
            if model_type_key_new_format in self._model_list:
                logger.warning("This model key format is deprecated: '{}'. Use '{}' instead.".format(model_type_key, model_type_key_new_format))
                model_type_key = model_type_key_new_format
            else:
                raise InvalidNet("Unknown model key '{}'. Also tried '{}' for backward compatibility.".format(model_type_key, model_type_key_new_format))
        self._model_args = self._model_list[model_type_key]

    def get_model_param(self, param):
        """
        Search in args and default_args for `param`. This permits searching for a default parameter
        from the model_list, after an Experiment has been built.
        Warning: this should be used as a last resort, when you need a param from an Experiment, before even building it.
        ```
        builder = ExperimentBuilder(...)
        batch_size = builder.get_model_param('batch_size')
        xp = builder.build(num_train_steps = n / batch_size)
        ```
        All protobuf default params are exposed once it's built.
        """
        if param in self._model_args.default_args:
            return self._model_args.default_args[param]
        else:
            logger.warn('Parameter not found in experiment builder: {}. Available model args are: {}'.format(param, self._model_args))

    @classmethod
    def load_model_list(cls):
        # Avoid to load it at the root of the module to avoid nested import loops
        cls._model_list = {}
        for key, args in model_list.model_list.items():
            assert key not in cls._model_list, "Duplicate model key, this should not happen"
            cls._model_list[key] = args

    def build(self, **kwargs):
        all_args = set()
        all_args.update(self._model_args.default_args.keys())
        all_args.update(kwargs.keys())
        used_args = set()
        xp = self._recursive_build_(Experiment, self._model_args.default_args, kwargs, used_args)
        unused_args = all_args - used_args
        if len(unused_args) > 0:
            raise Exception('Unused keyword argument: {}'.format(', '.join(unused_args)))
        return xp

    @staticmethod
    def _recursive_build_(protobuf_class, default_args, kwargs, used_args):
        real_args = {}

        unsed_default_args = default_args.keys() - set([f.name for f in protobuf_class.DESCRIPTOR.fields])
        if len(unsed_default_args) > 0:
            raise Exception('Unused default keyword argument: {}'.format(', '.join(unsed_default_args)))

        def strip_serializer(value):
            """Convert a serialier into a protobuf"""
            if isinstance(value, Serializer):
                return value._msg
            else:
                return value

        for field in protobuf_class.DESCRIPTOR.fields:
            if field.message_type is None or field.label == FieldDescriptor.LABEL_REPEATED:
                # there is only one possible value and kwargs has higher priority
                if field.name in kwargs:
                    real_args[field.name] = strip_serializer(kwargs[field.name])
                elif field.name in default_args:
                    real_args[field.name] = default_args[field.name]

            else:
                if field.name in kwargs:
                    real_args[field.name] = strip_serializer(kwargs[field.name])
                else:
                    if field.name in default_args or field.label == FieldDescriptor.LABEL_REQUIRED:
                        field_default_args = default_args[field.name] if field.name in default_args else {}
                        field_protobuf_class = class_helpers.load_proto_class_from_protobuf_descriptor(field.message_type)
                        if field_protobuf_class is None:
                            real_args[field.name] = field_default_args  # all field are expected to be scalar
                        else:
                            # This fields is a protobuf message, we build it recursively
                            real_args[field.name] = ExperimentBuilder._recursive_build_(field_protobuf_class, field_default_args, kwargs, used_args)

        for field_name in real_args:
            used_args.add(field_name)
        return protobuf_class(**real_args)
