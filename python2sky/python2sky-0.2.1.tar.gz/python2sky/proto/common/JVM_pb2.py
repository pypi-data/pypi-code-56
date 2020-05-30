# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: common/JVM.proto

from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

from proto.common import common_pb2 as common_dot_common__pb2

DESCRIPTOR = _descriptor.FileDescriptor(
  name='common/JVM.proto',
  package='',
  syntax='proto3',
  serialized_options=b'\n0org.apache.skywalking.apm.network.language.agentP\001\252\002\032SkyWalking.NetworkProtocol',
  serialized_pb=b'\n\x10\x63ommon/JVM.proto\x1a\x13\x63ommon/common.proto\"w\n\tJVMMetric\x12\x0c\n\x04time\x18\x01 \x01(\x03\x12\x11\n\x03\x63pu\x18\x02 \x01(\x0b\x32\x04.CPU\x12\x17\n\x06memory\x18\x03 \x03(\x0b\x32\x07.Memory\x12\x1f\n\nmemoryPool\x18\x04 \x03(\x0b\x32\x0b.MemoryPool\x12\x0f\n\x02gc\x18\x05 \x03(\x0b\x32\x03.GC\"T\n\x06Memory\x12\x0e\n\x06isHeap\x18\x01 \x01(\x08\x12\x0c\n\x04init\x18\x02 \x01(\x03\x12\x0b\n\x03max\x18\x03 \x01(\x03\x12\x0c\n\x04used\x18\x04 \x01(\x03\x12\x11\n\tcommitted\x18\x05 \x01(\x03\"`\n\nMemoryPool\x12\x17\n\x04type\x18\x01 \x01(\x0e\x32\t.PoolType\x12\x0c\n\x04init\x18\x02 \x01(\x03\x12\x0b\n\x03max\x18\x03 \x01(\x03\x12\x0c\n\x04used\x18\x04 \x01(\x03\x12\x10\n\x08\x63ommited\x18\x05 \x01(\x03\"<\n\x02GC\x12\x19\n\x06phrase\x18\x01 \x01(\x0e\x32\t.GCPhrase\x12\r\n\x05\x63ount\x18\x02 \x01(\x03\x12\x0c\n\x04time\x18\x03 \x01(\x03*\x80\x01\n\x08PoolType\x12\x14\n\x10\x43ODE_CACHE_USAGE\x10\x00\x12\x10\n\x0cNEWGEN_USAGE\x10\x01\x12\x10\n\x0cOLDGEN_USAGE\x10\x02\x12\x12\n\x0eSURVIVOR_USAGE\x10\x03\x12\x11\n\rPERMGEN_USAGE\x10\x04\x12\x13\n\x0fMETASPACE_USAGE\x10\x05*\x1c\n\x08GCPhrase\x12\x07\n\x03NEW\x10\x00\x12\x07\n\x03OLD\x10\x01\x42Q\n0org.apache.skywalking.apm.network.language.agentP\x01\xaa\x02\x1aSkyWalking.NetworkProtocolb\x06proto3'
  ,
  dependencies=[common_dot_common__pb2.DESCRIPTOR,])

_POOLTYPE = _descriptor.EnumDescriptor(
  name='PoolType',
  full_name='PoolType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CODE_CACHE_USAGE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NEWGEN_USAGE', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OLDGEN_USAGE', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SURVIVOR_USAGE', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PERMGEN_USAGE', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='METASPACE_USAGE', index=5, number=5,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=409,
  serialized_end=537,
)
_sym_db.RegisterEnumDescriptor(_POOLTYPE)

PoolType = enum_type_wrapper.EnumTypeWrapper(_POOLTYPE)
_GCPHRASE = _descriptor.EnumDescriptor(
  name='GCPhrase',
  full_name='GCPhrase',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NEW', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OLD', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=539,
  serialized_end=567,
)
_sym_db.RegisterEnumDescriptor(_GCPHRASE)

GCPhrase = enum_type_wrapper.EnumTypeWrapper(_GCPHRASE)
CODE_CACHE_USAGE = 0
NEWGEN_USAGE = 1
OLDGEN_USAGE = 2
SURVIVOR_USAGE = 3
PERMGEN_USAGE = 4
METASPACE_USAGE = 5
NEW = 0
OLD = 1



_JVMMETRIC = _descriptor.Descriptor(
  name='JVMMetric',
  full_name='JVMMetric',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='time', full_name='JVMMetric.time', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cpu', full_name='JVMMetric.cpu', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='memory', full_name='JVMMetric.memory', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='memoryPool', full_name='JVMMetric.memoryPool', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='gc', full_name='JVMMetric.gc', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=41,
  serialized_end=160,
)


_MEMORY = _descriptor.Descriptor(
  name='Memory',
  full_name='Memory',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='isHeap', full_name='Memory.isHeap', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='init', full_name='Memory.init', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='max', full_name='Memory.max', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='used', full_name='Memory.used', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='committed', full_name='Memory.committed', index=4,
      number=5, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=162,
  serialized_end=246,
)


_MEMORYPOOL = _descriptor.Descriptor(
  name='MemoryPool',
  full_name='MemoryPool',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='MemoryPool.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='init', full_name='MemoryPool.init', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='max', full_name='MemoryPool.max', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='used', full_name='MemoryPool.used', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='commited', full_name='MemoryPool.commited', index=4,
      number=5, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=248,
  serialized_end=344,
)


_GC = _descriptor.Descriptor(
  name='GC',
  full_name='GC',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='phrase', full_name='GC.phrase', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='count', full_name='GC.count', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='time', full_name='GC.time', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=346,
  serialized_end=406,
)

_JVMMETRIC.fields_by_name['cpu'].message_type = common_dot_common__pb2._CPU
_JVMMETRIC.fields_by_name['memory'].message_type = _MEMORY
_JVMMETRIC.fields_by_name['memoryPool'].message_type = _MEMORYPOOL
_JVMMETRIC.fields_by_name['gc'].message_type = _GC
_MEMORYPOOL.fields_by_name['type'].enum_type = _POOLTYPE
_GC.fields_by_name['phrase'].enum_type = _GCPHRASE
DESCRIPTOR.message_types_by_name['JVMMetric'] = _JVMMETRIC
DESCRIPTOR.message_types_by_name['Memory'] = _MEMORY
DESCRIPTOR.message_types_by_name['MemoryPool'] = _MEMORYPOOL
DESCRIPTOR.message_types_by_name['GC'] = _GC
DESCRIPTOR.enum_types_by_name['PoolType'] = _POOLTYPE
DESCRIPTOR.enum_types_by_name['GCPhrase'] = _GCPHRASE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

JVMMetric = _reflection.GeneratedProtocolMessageType('JVMMetric', (_message.Message,), {
  'DESCRIPTOR' : _JVMMETRIC,
  '__module__' : 'common.JVM_pb2'
  # @@protoc_insertion_point(class_scope:JVMMetric)
  })
_sym_db.RegisterMessage(JVMMetric)

Memory = _reflection.GeneratedProtocolMessageType('Memory', (_message.Message,), {
  'DESCRIPTOR' : _MEMORY,
  '__module__' : 'common.JVM_pb2'
  # @@protoc_insertion_point(class_scope:Memory)
  })
_sym_db.RegisterMessage(Memory)

MemoryPool = _reflection.GeneratedProtocolMessageType('MemoryPool', (_message.Message,), {
  'DESCRIPTOR' : _MEMORYPOOL,
  '__module__' : 'common.JVM_pb2'
  # @@protoc_insertion_point(class_scope:MemoryPool)
  })
_sym_db.RegisterMessage(MemoryPool)

GC = _reflection.GeneratedProtocolMessageType('GC', (_message.Message,), {
  'DESCRIPTOR' : _GC,
  '__module__' : 'common.JVM_pb2'
  # @@protoc_insertion_point(class_scope:GC)
  })
_sym_db.RegisterMessage(GC)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
