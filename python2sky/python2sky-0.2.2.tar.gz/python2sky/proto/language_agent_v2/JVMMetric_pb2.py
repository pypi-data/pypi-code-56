# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: language_agent_v2/JVMMetric.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from python2sky.proto.common import common_pb2 as common_dot_common__pb2
from python2sky.proto.common import JVM_pb2 as common_dot_JVM__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='language_agent_v2/JVMMetric.proto',
  package='',
  syntax='proto3',
  serialized_options=b'\n3org.apache.skywalking.apm.network.language.agent.v2P\001\252\002\032SkyWalking.NetworkProtocol',
  serialized_pb=b'\n!language_agent_v2/JVMMetric.proto\x1a\x13\x63ommon/common.proto\x1a\x10\x63ommon/JVM.proto\"M\n\x13JVMMetricCollection\x12\x1b\n\x07metrics\x18\x01 \x03(\x0b\x32\n.JVMMetric\x12\x19\n\x11serviceInstanceId\x18\x02 \x01(\x05\x32\x46\n\x16JVMMetricReportService\x12,\n\x07\x63ollect\x12\x14.JVMMetricCollection\x1a\t.Commands\"\x00\x42T\n3org.apache.skywalking.apm.network.language.agent.v2P\x01\xaa\x02\x1aSkyWalking.NetworkProtocolb\x06proto3'
  ,
  dependencies=[common_dot_common__pb2.DESCRIPTOR,common_dot_JVM__pb2.DESCRIPTOR,])




_JVMMETRICCOLLECTION = _descriptor.Descriptor(
  name='JVMMetricCollection',
  full_name='JVMMetricCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='metrics', full_name='JVMMetricCollection.metrics', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='serviceInstanceId', full_name='JVMMetricCollection.serviceInstanceId', index=1,
      number=2, type=5, cpp_type=1, label=1,
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
  serialized_start=76,
  serialized_end=153,
)

_JVMMETRICCOLLECTION.fields_by_name['metrics'].message_type = common_dot_JVM__pb2._JVMMETRIC
DESCRIPTOR.message_types_by_name['JVMMetricCollection'] = _JVMMETRICCOLLECTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

JVMMetricCollection = _reflection.GeneratedProtocolMessageType('JVMMetricCollection', (_message.Message,), {
  'DESCRIPTOR' : _JVMMETRICCOLLECTION,
  '__module__' : 'language_agent_v2.JVMMetric_pb2'
  # @@protoc_insertion_point(class_scope:JVMMetricCollection)
  })
_sym_db.RegisterMessage(JVMMetricCollection)


DESCRIPTOR._options = None

_JVMMETRICREPORTSERVICE = _descriptor.ServiceDescriptor(
  name='JVMMetricReportService',
  full_name='JVMMetricReportService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=155,
  serialized_end=225,
  methods=[
  _descriptor.MethodDescriptor(
    name='collect',
    full_name='JVMMetricReportService.collect',
    index=0,
    containing_service=None,
    input_type=_JVMMETRICCOLLECTION,
    output_type=common_dot_common__pb2._COMMANDS,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_JVMMETRICREPORTSERVICE)

DESCRIPTOR.services_by_name['JVMMetricReportService'] = _JVMMETRICREPORTSERVICE

# @@protoc_insertion_point(module_scope)
