# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: register/InstancePing.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from python2sky.proto.common import common_pb2 as common_dot_common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='register/InstancePing.proto',
  package='',
  syntax='proto3',
  serialized_options=b'\n-org.apache.skywalking.apm.network.register.v2P\001\252\002\032SkyWalking.NetworkProtocol',
  serialized_pb=b'\n\x1bregister/InstancePing.proto\x1a\x13\x63ommon/common.proto\"^\n\x16ServiceInstancePingPkg\x12\x19\n\x11serviceInstanceId\x18\x01 \x01(\x05\x12\x0c\n\x04time\x18\x02 \x01(\x03\x12\x1b\n\x13serviceInstanceUUID\x18\x03 \x01(\t2E\n\x13ServiceInstancePing\x12.\n\x06\x64oPing\x12\x17.ServiceInstancePingPkg\x1a\t.Commands\"\x00\x42N\n-org.apache.skywalking.apm.network.register.v2P\x01\xaa\x02\x1aSkyWalking.NetworkProtocolb\x06proto3'
  ,
  dependencies=[common_dot_common__pb2.DESCRIPTOR,])




_SERVICEINSTANCEPINGPKG = _descriptor.Descriptor(
  name='ServiceInstancePingPkg',
  full_name='ServiceInstancePingPkg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='serviceInstanceId', full_name='ServiceInstancePingPkg.serviceInstanceId', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='time', full_name='ServiceInstancePingPkg.time', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='serviceInstanceUUID', full_name='ServiceInstancePingPkg.serviceInstanceUUID', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=52,
  serialized_end=146,
)

DESCRIPTOR.message_types_by_name['ServiceInstancePingPkg'] = _SERVICEINSTANCEPINGPKG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ServiceInstancePingPkg = _reflection.GeneratedProtocolMessageType('ServiceInstancePingPkg', (_message.Message,), {
  'DESCRIPTOR' : _SERVICEINSTANCEPINGPKG,
  '__module__' : 'register.InstancePing_pb2'
  # @@protoc_insertion_point(class_scope:ServiceInstancePingPkg)
  })
_sym_db.RegisterMessage(ServiceInstancePingPkg)


DESCRIPTOR._options = None

_SERVICEINSTANCEPING = _descriptor.ServiceDescriptor(
  name='ServiceInstancePing',
  full_name='ServiceInstancePing',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=148,
  serialized_end=217,
  methods=[
  _descriptor.MethodDescriptor(
    name='doPing',
    full_name='ServiceInstancePing.doPing',
    index=0,
    containing_service=None,
    input_type=_SERVICEINSTANCEPINGPKG,
    output_type=common_dot_common__pb2._COMMANDS,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_SERVICEINSTANCEPING)

DESCRIPTOR.services_by_name['ServiceInstancePing'] = _SERVICEINSTANCEPING

# @@protoc_insertion_point(module_scope)
