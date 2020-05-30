# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: param.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import mavsdk_options_pb2 as mavsdk__options__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='param.proto',
  package='mavsdk.rpc.param',
  syntax='proto3',
  serialized_options=b'\n\017io.mavsdk.paramB\nParamProto',
  serialized_pb=b'\n\x0bparam.proto\x12\x10mavsdk.rpc.param\x1a\x14mavsdk_options.proto\"\"\n\x12GetParamIntRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"Y\n\x13GetParamIntResponse\x12\x33\n\x0cparam_result\x18\x01 \x01(\x0b\x32\x1d.mavsdk.rpc.param.ParamResult\x12\r\n\x05value\x18\x02 \x01(\x05\"1\n\x12SetParamIntRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05\"J\n\x13SetParamIntResponse\x12\x33\n\x0cparam_result\x18\x01 \x01(\x0b\x32\x1d.mavsdk.rpc.param.ParamResult\"$\n\x14GetParamFloatRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"[\n\x15GetParamFloatResponse\x12\x33\n\x0cparam_result\x18\x01 \x01(\x0b\x32\x1d.mavsdk.rpc.param.ParamResult\x12\r\n\x05value\x18\x02 \x01(\x02\"3\n\x14SetParamFloatRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x02\"L\n\x15SetParamFloatResponse\x12\x33\n\x0cparam_result\x18\x01 \x01(\x0b\x32\x1d.mavsdk.rpc.param.ParamResult\"\xf2\x01\n\x0bParamResult\x12\x34\n\x06result\x18\x01 \x01(\x0e\x32$.mavsdk.rpc.param.ParamResult.Result\x12\x12\n\nresult_str\x18\x02 \x01(\t\"\x98\x01\n\x06Result\x12\x12\n\x0eRESULT_UNKNOWN\x10\x00\x12\x12\n\x0eRESULT_SUCCESS\x10\x01\x12\x12\n\x0eRESULT_TIMEOUT\x10\x02\x12\x1b\n\x17RESULT_CONNECTION_ERROR\x10\x03\x12\x15\n\x11RESULT_WRONG_TYPE\x10\x04\x12\x1e\n\x1aRESULT_PARAM_NAME_TOO_LONG\x10\x05\x32\xa2\x03\n\x0cParamService\x12`\n\x0bGetParamInt\x12$.mavsdk.rpc.param.GetParamIntRequest\x1a%.mavsdk.rpc.param.GetParamIntResponse\"\x04\x80\xb5\x18\x01\x12`\n\x0bSetParamInt\x12$.mavsdk.rpc.param.SetParamIntRequest\x1a%.mavsdk.rpc.param.SetParamIntResponse\"\x04\x80\xb5\x18\x01\x12\x66\n\rGetParamFloat\x12&.mavsdk.rpc.param.GetParamFloatRequest\x1a\'.mavsdk.rpc.param.GetParamFloatResponse\"\x04\x80\xb5\x18\x01\x12\x66\n\rSetParamFloat\x12&.mavsdk.rpc.param.SetParamFloatRequest\x1a\'.mavsdk.rpc.param.SetParamFloatResponse\"\x04\x80\xb5\x18\x01\x42\x1d\n\x0fio.mavsdk.paramB\nParamProtob\x06proto3'
  ,
  dependencies=[mavsdk__options__pb2.DESCRIPTOR,])



_PARAMRESULT_RESULT = _descriptor.EnumDescriptor(
  name='Result',
  full_name='mavsdk.rpc.param.ParamResult.Result',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='RESULT_UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RESULT_SUCCESS', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RESULT_TIMEOUT', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RESULT_CONNECTION_ERROR', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RESULT_WRONG_TYPE', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RESULT_PARAM_NAME_TOO_LONG', index=5, number=5,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=662,
  serialized_end=814,
)
_sym_db.RegisterEnumDescriptor(_PARAMRESULT_RESULT)


_GETPARAMINTREQUEST = _descriptor.Descriptor(
  name='GetParamIntRequest',
  full_name='mavsdk.rpc.param.GetParamIntRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='mavsdk.rpc.param.GetParamIntRequest.name', index=0,
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
  serialized_start=55,
  serialized_end=89,
)


_GETPARAMINTRESPONSE = _descriptor.Descriptor(
  name='GetParamIntResponse',
  full_name='mavsdk.rpc.param.GetParamIntResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='param_result', full_name='mavsdk.rpc.param.GetParamIntResponse.param_result', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='mavsdk.rpc.param.GetParamIntResponse.value', index=1,
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
  serialized_start=91,
  serialized_end=180,
)


_SETPARAMINTREQUEST = _descriptor.Descriptor(
  name='SetParamIntRequest',
  full_name='mavsdk.rpc.param.SetParamIntRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='mavsdk.rpc.param.SetParamIntRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='mavsdk.rpc.param.SetParamIntRequest.value', index=1,
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
  serialized_start=182,
  serialized_end=231,
)


_SETPARAMINTRESPONSE = _descriptor.Descriptor(
  name='SetParamIntResponse',
  full_name='mavsdk.rpc.param.SetParamIntResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='param_result', full_name='mavsdk.rpc.param.SetParamIntResponse.param_result', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  ],
  serialized_start=233,
  serialized_end=307,
)


_GETPARAMFLOATREQUEST = _descriptor.Descriptor(
  name='GetParamFloatRequest',
  full_name='mavsdk.rpc.param.GetParamFloatRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='mavsdk.rpc.param.GetParamFloatRequest.name', index=0,
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
  serialized_start=309,
  serialized_end=345,
)


_GETPARAMFLOATRESPONSE = _descriptor.Descriptor(
  name='GetParamFloatResponse',
  full_name='mavsdk.rpc.param.GetParamFloatResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='param_result', full_name='mavsdk.rpc.param.GetParamFloatResponse.param_result', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='mavsdk.rpc.param.GetParamFloatResponse.value', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=347,
  serialized_end=438,
)


_SETPARAMFLOATREQUEST = _descriptor.Descriptor(
  name='SetParamFloatRequest',
  full_name='mavsdk.rpc.param.SetParamFloatRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='mavsdk.rpc.param.SetParamFloatRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='mavsdk.rpc.param.SetParamFloatRequest.value', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=440,
  serialized_end=491,
)


_SETPARAMFLOATRESPONSE = _descriptor.Descriptor(
  name='SetParamFloatResponse',
  full_name='mavsdk.rpc.param.SetParamFloatResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='param_result', full_name='mavsdk.rpc.param.SetParamFloatResponse.param_result', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  ],
  serialized_start=493,
  serialized_end=569,
)


_PARAMRESULT = _descriptor.Descriptor(
  name='ParamResult',
  full_name='mavsdk.rpc.param.ParamResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='mavsdk.rpc.param.ParamResult.result', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='result_str', full_name='mavsdk.rpc.param.ParamResult.result_str', index=1,
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
    _PARAMRESULT_RESULT,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=572,
  serialized_end=814,
)

_GETPARAMINTRESPONSE.fields_by_name['param_result'].message_type = _PARAMRESULT
_SETPARAMINTRESPONSE.fields_by_name['param_result'].message_type = _PARAMRESULT
_GETPARAMFLOATRESPONSE.fields_by_name['param_result'].message_type = _PARAMRESULT
_SETPARAMFLOATRESPONSE.fields_by_name['param_result'].message_type = _PARAMRESULT
_PARAMRESULT.fields_by_name['result'].enum_type = _PARAMRESULT_RESULT
_PARAMRESULT_RESULT.containing_type = _PARAMRESULT
DESCRIPTOR.message_types_by_name['GetParamIntRequest'] = _GETPARAMINTREQUEST
DESCRIPTOR.message_types_by_name['GetParamIntResponse'] = _GETPARAMINTRESPONSE
DESCRIPTOR.message_types_by_name['SetParamIntRequest'] = _SETPARAMINTREQUEST
DESCRIPTOR.message_types_by_name['SetParamIntResponse'] = _SETPARAMINTRESPONSE
DESCRIPTOR.message_types_by_name['GetParamFloatRequest'] = _GETPARAMFLOATREQUEST
DESCRIPTOR.message_types_by_name['GetParamFloatResponse'] = _GETPARAMFLOATRESPONSE
DESCRIPTOR.message_types_by_name['SetParamFloatRequest'] = _SETPARAMFLOATREQUEST
DESCRIPTOR.message_types_by_name['SetParamFloatResponse'] = _SETPARAMFLOATRESPONSE
DESCRIPTOR.message_types_by_name['ParamResult'] = _PARAMRESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetParamIntRequest = _reflection.GeneratedProtocolMessageType('GetParamIntRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETPARAMINTREQUEST,
  '__module__' : 'param_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.param.GetParamIntRequest)
  })
_sym_db.RegisterMessage(GetParamIntRequest)

GetParamIntResponse = _reflection.GeneratedProtocolMessageType('GetParamIntResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETPARAMINTRESPONSE,
  '__module__' : 'param_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.param.GetParamIntResponse)
  })
_sym_db.RegisterMessage(GetParamIntResponse)

SetParamIntRequest = _reflection.GeneratedProtocolMessageType('SetParamIntRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETPARAMINTREQUEST,
  '__module__' : 'param_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.param.SetParamIntRequest)
  })
_sym_db.RegisterMessage(SetParamIntRequest)

SetParamIntResponse = _reflection.GeneratedProtocolMessageType('SetParamIntResponse', (_message.Message,), {
  'DESCRIPTOR' : _SETPARAMINTRESPONSE,
  '__module__' : 'param_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.param.SetParamIntResponse)
  })
_sym_db.RegisterMessage(SetParamIntResponse)

GetParamFloatRequest = _reflection.GeneratedProtocolMessageType('GetParamFloatRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETPARAMFLOATREQUEST,
  '__module__' : 'param_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.param.GetParamFloatRequest)
  })
_sym_db.RegisterMessage(GetParamFloatRequest)

GetParamFloatResponse = _reflection.GeneratedProtocolMessageType('GetParamFloatResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETPARAMFLOATRESPONSE,
  '__module__' : 'param_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.param.GetParamFloatResponse)
  })
_sym_db.RegisterMessage(GetParamFloatResponse)

SetParamFloatRequest = _reflection.GeneratedProtocolMessageType('SetParamFloatRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETPARAMFLOATREQUEST,
  '__module__' : 'param_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.param.SetParamFloatRequest)
  })
_sym_db.RegisterMessage(SetParamFloatRequest)

SetParamFloatResponse = _reflection.GeneratedProtocolMessageType('SetParamFloatResponse', (_message.Message,), {
  'DESCRIPTOR' : _SETPARAMFLOATRESPONSE,
  '__module__' : 'param_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.param.SetParamFloatResponse)
  })
_sym_db.RegisterMessage(SetParamFloatResponse)

ParamResult = _reflection.GeneratedProtocolMessageType('ParamResult', (_message.Message,), {
  'DESCRIPTOR' : _PARAMRESULT,
  '__module__' : 'param_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.param.ParamResult)
  })
_sym_db.RegisterMessage(ParamResult)


DESCRIPTOR._options = None

_PARAMSERVICE = _descriptor.ServiceDescriptor(
  name='ParamService',
  full_name='mavsdk.rpc.param.ParamService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=817,
  serialized_end=1235,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetParamInt',
    full_name='mavsdk.rpc.param.ParamService.GetParamInt',
    index=0,
    containing_service=None,
    input_type=_GETPARAMINTREQUEST,
    output_type=_GETPARAMINTRESPONSE,
    serialized_options=b'\200\265\030\001',
  ),
  _descriptor.MethodDescriptor(
    name='SetParamInt',
    full_name='mavsdk.rpc.param.ParamService.SetParamInt',
    index=1,
    containing_service=None,
    input_type=_SETPARAMINTREQUEST,
    output_type=_SETPARAMINTRESPONSE,
    serialized_options=b'\200\265\030\001',
  ),
  _descriptor.MethodDescriptor(
    name='GetParamFloat',
    full_name='mavsdk.rpc.param.ParamService.GetParamFloat',
    index=2,
    containing_service=None,
    input_type=_GETPARAMFLOATREQUEST,
    output_type=_GETPARAMFLOATRESPONSE,
    serialized_options=b'\200\265\030\001',
  ),
  _descriptor.MethodDescriptor(
    name='SetParamFloat',
    full_name='mavsdk.rpc.param.ParamService.SetParamFloat',
    index=3,
    containing_service=None,
    input_type=_SETPARAMFLOATREQUEST,
    output_type=_SETPARAMFLOATRESPONSE,
    serialized_options=b'\200\265\030\001',
  ),
])
_sym_db.RegisterServiceDescriptor(_PARAMSERVICE)

DESCRIPTOR.services_by_name['ParamService'] = _PARAMSERVICE

# @@protoc_insertion_point(module_scope)
