'''
This module uses decorators to accomplish serialization and deserialization
of types. There are
three decorators associated with the API. One assigns a function to serialize
a specific type, another does the same for deserialization, and a final
decorator allows a type (class) to serialize itself.

In the example links, please expand the code in the example documentation. It is best to
expand the code at the top of the page to see all the decorators in use.
'''

from .registry import (register_deserializer, register_serializer,
                       to_serializable, from_serializable)
from .decorator import deserializer, serialization, serializer
from .signatures import JSONSerializable
from .version import MAJOR_VERSION, MINOR_VERSION, BUILDNUMBER

version = f'{MAJOR_VERSION}.{MINOR_VERSION}.{BUILDNUMBER}'

__all__ = [
    'deserializer',
    'serializer',
    'serialization',
    'JSONSerializable',
    'version',
]
