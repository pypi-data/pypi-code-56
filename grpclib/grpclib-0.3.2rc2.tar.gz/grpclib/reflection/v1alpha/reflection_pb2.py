# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grpclib/reflection/v1alpha/reflection.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='grpclib/reflection/v1alpha/reflection.proto',
  package='grpc.reflection.v1alpha',
  syntax='proto3',
  serialized_options=b'\n\032io.grpc.reflection.v1alphaB\025ServerReflectionProtoP\001\270\001\001',
  serialized_pb=b'\n+grpclib/reflection/v1alpha/reflection.proto\x12\x17grpc.reflection.v1alpha\"\x8a\x02\n\x17ServerReflectionRequest\x12\x0c\n\x04host\x18\x01 \x01(\t\x12\x1a\n\x10\x66ile_by_filename\x18\x03 \x01(\tH\x00\x12 \n\x16\x66ile_containing_symbol\x18\x04 \x01(\tH\x00\x12N\n\x19\x66ile_containing_extension\x18\x05 \x01(\x0b\x32).grpc.reflection.v1alpha.ExtensionRequestH\x00\x12\'\n\x1d\x61ll_extension_numbers_of_type\x18\x06 \x01(\tH\x00\x12\x17\n\rlist_services\x18\x07 \x01(\tH\x00\x42\x11\n\x0fmessage_request\"E\n\x10\x45xtensionRequest\x12\x17\n\x0f\x63ontaining_type\x18\x01 \x01(\t\x12\x18\n\x10\x65xtension_number\x18\x02 \x01(\x05\"\xd1\x03\n\x18ServerReflectionResponse\x12\x12\n\nvalid_host\x18\x01 \x01(\t\x12J\n\x10original_request\x18\x02 \x01(\x0b\x32\x30.grpc.reflection.v1alpha.ServerReflectionRequest\x12S\n\x18\x66ile_descriptor_response\x18\x04 \x01(\x0b\x32/.grpc.reflection.v1alpha.FileDescriptorResponseH\x00\x12Z\n\x1e\x61ll_extension_numbers_response\x18\x05 \x01(\x0b\x32\x30.grpc.reflection.v1alpha.ExtensionNumberResponseH\x00\x12N\n\x16list_services_response\x18\x06 \x01(\x0b\x32,.grpc.reflection.v1alpha.ListServiceResponseH\x00\x12@\n\x0e\x65rror_response\x18\x07 \x01(\x0b\x32&.grpc.reflection.v1alpha.ErrorResponseH\x00\x42\x12\n\x10message_response\"7\n\x16\x46ileDescriptorResponse\x12\x1d\n\x15\x66ile_descriptor_proto\x18\x01 \x03(\x0c\"K\n\x17\x45xtensionNumberResponse\x12\x16\n\x0e\x62\x61se_type_name\x18\x01 \x01(\t\x12\x18\n\x10\x65xtension_number\x18\x02 \x03(\x05\"P\n\x13ListServiceResponse\x12\x39\n\x07service\x18\x01 \x03(\x0b\x32(.grpc.reflection.v1alpha.ServiceResponse\"\x1f\n\x0fServiceResponse\x12\x0c\n\x04name\x18\x01 \x01(\t\":\n\rErrorResponse\x12\x12\n\nerror_code\x18\x01 \x01(\x05\x12\x15\n\rerror_message\x18\x02 \x01(\t2\x93\x01\n\x10ServerReflection\x12\x7f\n\x14ServerReflectionInfo\x12\x30.grpc.reflection.v1alpha.ServerReflectionRequest\x1a\x31.grpc.reflection.v1alpha.ServerReflectionResponse(\x01\x30\x01\x42\x38\n\x1aio.grpc.reflection.v1alphaB\x15ServerReflectionProtoP\x01\xb8\x01\x01\x62\x06proto3'
)




_SERVERREFLECTIONREQUEST = _descriptor.Descriptor(
  name='ServerReflectionRequest',
  full_name='grpc.reflection.v1alpha.ServerReflectionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='host', full_name='grpc.reflection.v1alpha.ServerReflectionRequest.host', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='file_by_filename', full_name='grpc.reflection.v1alpha.ServerReflectionRequest.file_by_filename', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='file_containing_symbol', full_name='grpc.reflection.v1alpha.ServerReflectionRequest.file_containing_symbol', index=2,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='file_containing_extension', full_name='grpc.reflection.v1alpha.ServerReflectionRequest.file_containing_extension', index=3,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='all_extension_numbers_of_type', full_name='grpc.reflection.v1alpha.ServerReflectionRequest.all_extension_numbers_of_type', index=4,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='list_services', full_name='grpc.reflection.v1alpha.ServerReflectionRequest.list_services', index=5,
      number=7, type=9, cpp_type=9, label=1,
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
    _descriptor.OneofDescriptor(
      name='message_request', full_name='grpc.reflection.v1alpha.ServerReflectionRequest.message_request',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=73,
  serialized_end=339,
)


_EXTENSIONREQUEST = _descriptor.Descriptor(
  name='ExtensionRequest',
  full_name='grpc.reflection.v1alpha.ExtensionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='containing_type', full_name='grpc.reflection.v1alpha.ExtensionRequest.containing_type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='extension_number', full_name='grpc.reflection.v1alpha.ExtensionRequest.extension_number', index=1,
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
  serialized_start=341,
  serialized_end=410,
)


_SERVERREFLECTIONRESPONSE = _descriptor.Descriptor(
  name='ServerReflectionResponse',
  full_name='grpc.reflection.v1alpha.ServerReflectionResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='valid_host', full_name='grpc.reflection.v1alpha.ServerReflectionResponse.valid_host', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='original_request', full_name='grpc.reflection.v1alpha.ServerReflectionResponse.original_request', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='file_descriptor_response', full_name='grpc.reflection.v1alpha.ServerReflectionResponse.file_descriptor_response', index=2,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='all_extension_numbers_response', full_name='grpc.reflection.v1alpha.ServerReflectionResponse.all_extension_numbers_response', index=3,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='list_services_response', full_name='grpc.reflection.v1alpha.ServerReflectionResponse.list_services_response', index=4,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='error_response', full_name='grpc.reflection.v1alpha.ServerReflectionResponse.error_response', index=5,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
    _descriptor.OneofDescriptor(
      name='message_response', full_name='grpc.reflection.v1alpha.ServerReflectionResponse.message_response',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=413,
  serialized_end=878,
)


_FILEDESCRIPTORRESPONSE = _descriptor.Descriptor(
  name='FileDescriptorResponse',
  full_name='grpc.reflection.v1alpha.FileDescriptorResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='file_descriptor_proto', full_name='grpc.reflection.v1alpha.FileDescriptorResponse.file_descriptor_proto', index=0,
      number=1, type=12, cpp_type=9, label=3,
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
  serialized_start=880,
  serialized_end=935,
)


_EXTENSIONNUMBERRESPONSE = _descriptor.Descriptor(
  name='ExtensionNumberResponse',
  full_name='grpc.reflection.v1alpha.ExtensionNumberResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='base_type_name', full_name='grpc.reflection.v1alpha.ExtensionNumberResponse.base_type_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='extension_number', full_name='grpc.reflection.v1alpha.ExtensionNumberResponse.extension_number', index=1,
      number=2, type=5, cpp_type=1, label=3,
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
  serialized_start=937,
  serialized_end=1012,
)


_LISTSERVICERESPONSE = _descriptor.Descriptor(
  name='ListServiceResponse',
  full_name='grpc.reflection.v1alpha.ListServiceResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='service', full_name='grpc.reflection.v1alpha.ListServiceResponse.service', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=1014,
  serialized_end=1094,
)


_SERVICERESPONSE = _descriptor.Descriptor(
  name='ServiceResponse',
  full_name='grpc.reflection.v1alpha.ServiceResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='grpc.reflection.v1alpha.ServiceResponse.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=1096,
  serialized_end=1127,
)


_ERRORRESPONSE = _descriptor.Descriptor(
  name='ErrorResponse',
  full_name='grpc.reflection.v1alpha.ErrorResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='error_code', full_name='grpc.reflection.v1alpha.ErrorResponse.error_code', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='error_message', full_name='grpc.reflection.v1alpha.ErrorResponse.error_message', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=1129,
  serialized_end=1187,
)

_SERVERREFLECTIONREQUEST.fields_by_name['file_containing_extension'].message_type = _EXTENSIONREQUEST
_SERVERREFLECTIONREQUEST.oneofs_by_name['message_request'].fields.append(
  _SERVERREFLECTIONREQUEST.fields_by_name['file_by_filename'])
_SERVERREFLECTIONREQUEST.fields_by_name['file_by_filename'].containing_oneof = _SERVERREFLECTIONREQUEST.oneofs_by_name['message_request']
_SERVERREFLECTIONREQUEST.oneofs_by_name['message_request'].fields.append(
  _SERVERREFLECTIONREQUEST.fields_by_name['file_containing_symbol'])
_SERVERREFLECTIONREQUEST.fields_by_name['file_containing_symbol'].containing_oneof = _SERVERREFLECTIONREQUEST.oneofs_by_name['message_request']
_SERVERREFLECTIONREQUEST.oneofs_by_name['message_request'].fields.append(
  _SERVERREFLECTIONREQUEST.fields_by_name['file_containing_extension'])
_SERVERREFLECTIONREQUEST.fields_by_name['file_containing_extension'].containing_oneof = _SERVERREFLECTIONREQUEST.oneofs_by_name['message_request']
_SERVERREFLECTIONREQUEST.oneofs_by_name['message_request'].fields.append(
  _SERVERREFLECTIONREQUEST.fields_by_name['all_extension_numbers_of_type'])
_SERVERREFLECTIONREQUEST.fields_by_name['all_extension_numbers_of_type'].containing_oneof = _SERVERREFLECTIONREQUEST.oneofs_by_name['message_request']
_SERVERREFLECTIONREQUEST.oneofs_by_name['message_request'].fields.append(
  _SERVERREFLECTIONREQUEST.fields_by_name['list_services'])
_SERVERREFLECTIONREQUEST.fields_by_name['list_services'].containing_oneof = _SERVERREFLECTIONREQUEST.oneofs_by_name['message_request']
_SERVERREFLECTIONRESPONSE.fields_by_name['original_request'].message_type = _SERVERREFLECTIONREQUEST
_SERVERREFLECTIONRESPONSE.fields_by_name['file_descriptor_response'].message_type = _FILEDESCRIPTORRESPONSE
_SERVERREFLECTIONRESPONSE.fields_by_name['all_extension_numbers_response'].message_type = _EXTENSIONNUMBERRESPONSE
_SERVERREFLECTIONRESPONSE.fields_by_name['list_services_response'].message_type = _LISTSERVICERESPONSE
_SERVERREFLECTIONRESPONSE.fields_by_name['error_response'].message_type = _ERRORRESPONSE
_SERVERREFLECTIONRESPONSE.oneofs_by_name['message_response'].fields.append(
  _SERVERREFLECTIONRESPONSE.fields_by_name['file_descriptor_response'])
_SERVERREFLECTIONRESPONSE.fields_by_name['file_descriptor_response'].containing_oneof = _SERVERREFLECTIONRESPONSE.oneofs_by_name['message_response']
_SERVERREFLECTIONRESPONSE.oneofs_by_name['message_response'].fields.append(
  _SERVERREFLECTIONRESPONSE.fields_by_name['all_extension_numbers_response'])
_SERVERREFLECTIONRESPONSE.fields_by_name['all_extension_numbers_response'].containing_oneof = _SERVERREFLECTIONRESPONSE.oneofs_by_name['message_response']
_SERVERREFLECTIONRESPONSE.oneofs_by_name['message_response'].fields.append(
  _SERVERREFLECTIONRESPONSE.fields_by_name['list_services_response'])
_SERVERREFLECTIONRESPONSE.fields_by_name['list_services_response'].containing_oneof = _SERVERREFLECTIONRESPONSE.oneofs_by_name['message_response']
_SERVERREFLECTIONRESPONSE.oneofs_by_name['message_response'].fields.append(
  _SERVERREFLECTIONRESPONSE.fields_by_name['error_response'])
_SERVERREFLECTIONRESPONSE.fields_by_name['error_response'].containing_oneof = _SERVERREFLECTIONRESPONSE.oneofs_by_name['message_response']
_LISTSERVICERESPONSE.fields_by_name['service'].message_type = _SERVICERESPONSE
DESCRIPTOR.message_types_by_name['ServerReflectionRequest'] = _SERVERREFLECTIONREQUEST
DESCRIPTOR.message_types_by_name['ExtensionRequest'] = _EXTENSIONREQUEST
DESCRIPTOR.message_types_by_name['ServerReflectionResponse'] = _SERVERREFLECTIONRESPONSE
DESCRIPTOR.message_types_by_name['FileDescriptorResponse'] = _FILEDESCRIPTORRESPONSE
DESCRIPTOR.message_types_by_name['ExtensionNumberResponse'] = _EXTENSIONNUMBERRESPONSE
DESCRIPTOR.message_types_by_name['ListServiceResponse'] = _LISTSERVICERESPONSE
DESCRIPTOR.message_types_by_name['ServiceResponse'] = _SERVICERESPONSE
DESCRIPTOR.message_types_by_name['ErrorResponse'] = _ERRORRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ServerReflectionRequest = _reflection.GeneratedProtocolMessageType('ServerReflectionRequest', (_message.Message,), {
  'DESCRIPTOR' : _SERVERREFLECTIONREQUEST,
  '__module__' : 'grpclib.reflection.v1alpha.reflection_pb2'
  # @@protoc_insertion_point(class_scope:grpc.reflection.v1alpha.ServerReflectionRequest)
  })
_sym_db.RegisterMessage(ServerReflectionRequest)

ExtensionRequest = _reflection.GeneratedProtocolMessageType('ExtensionRequest', (_message.Message,), {
  'DESCRIPTOR' : _EXTENSIONREQUEST,
  '__module__' : 'grpclib.reflection.v1alpha.reflection_pb2'
  # @@protoc_insertion_point(class_scope:grpc.reflection.v1alpha.ExtensionRequest)
  })
_sym_db.RegisterMessage(ExtensionRequest)

ServerReflectionResponse = _reflection.GeneratedProtocolMessageType('ServerReflectionResponse', (_message.Message,), {
  'DESCRIPTOR' : _SERVERREFLECTIONRESPONSE,
  '__module__' : 'grpclib.reflection.v1alpha.reflection_pb2'
  # @@protoc_insertion_point(class_scope:grpc.reflection.v1alpha.ServerReflectionResponse)
  })
_sym_db.RegisterMessage(ServerReflectionResponse)

FileDescriptorResponse = _reflection.GeneratedProtocolMessageType('FileDescriptorResponse', (_message.Message,), {
  'DESCRIPTOR' : _FILEDESCRIPTORRESPONSE,
  '__module__' : 'grpclib.reflection.v1alpha.reflection_pb2'
  # @@protoc_insertion_point(class_scope:grpc.reflection.v1alpha.FileDescriptorResponse)
  })
_sym_db.RegisterMessage(FileDescriptorResponse)

ExtensionNumberResponse = _reflection.GeneratedProtocolMessageType('ExtensionNumberResponse', (_message.Message,), {
  'DESCRIPTOR' : _EXTENSIONNUMBERRESPONSE,
  '__module__' : 'grpclib.reflection.v1alpha.reflection_pb2'
  # @@protoc_insertion_point(class_scope:grpc.reflection.v1alpha.ExtensionNumberResponse)
  })
_sym_db.RegisterMessage(ExtensionNumberResponse)

ListServiceResponse = _reflection.GeneratedProtocolMessageType('ListServiceResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTSERVICERESPONSE,
  '__module__' : 'grpclib.reflection.v1alpha.reflection_pb2'
  # @@protoc_insertion_point(class_scope:grpc.reflection.v1alpha.ListServiceResponse)
  })
_sym_db.RegisterMessage(ListServiceResponse)

ServiceResponse = _reflection.GeneratedProtocolMessageType('ServiceResponse', (_message.Message,), {
  'DESCRIPTOR' : _SERVICERESPONSE,
  '__module__' : 'grpclib.reflection.v1alpha.reflection_pb2'
  # @@protoc_insertion_point(class_scope:grpc.reflection.v1alpha.ServiceResponse)
  })
_sym_db.RegisterMessage(ServiceResponse)

ErrorResponse = _reflection.GeneratedProtocolMessageType('ErrorResponse', (_message.Message,), {
  'DESCRIPTOR' : _ERRORRESPONSE,
  '__module__' : 'grpclib.reflection.v1alpha.reflection_pb2'
  # @@protoc_insertion_point(class_scope:grpc.reflection.v1alpha.ErrorResponse)
  })
_sym_db.RegisterMessage(ErrorResponse)


DESCRIPTOR._options = None

_SERVERREFLECTION = _descriptor.ServiceDescriptor(
  name='ServerReflection',
  full_name='grpc.reflection.v1alpha.ServerReflection',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1190,
  serialized_end=1337,
  methods=[
  _descriptor.MethodDescriptor(
    name='ServerReflectionInfo',
    full_name='grpc.reflection.v1alpha.ServerReflection.ServerReflectionInfo',
    index=0,
    containing_service=None,
    input_type=_SERVERREFLECTIONREQUEST,
    output_type=_SERVERREFLECTIONRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_SERVERREFLECTION)

DESCRIPTOR.services_by_name['ServerReflection'] = _SERVERREFLECTION

# @@protoc_insertion_point(module_scope)
