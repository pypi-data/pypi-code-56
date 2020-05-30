# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: server_configure.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='server_configure.proto',
  package='baidu.paddle_serving.configure',
  syntax='proto2',
  serialized_pb=_b('\n\x16server_configure.proto\x12\x1e\x62\x61idu.paddle_serving.configure\"\xbf\x04\n\nEngineDesc\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x0c\n\x04type\x18\x02 \x02(\t\x12\x17\n\x0freloadable_meta\x18\x03 \x02(\t\x12\x17\n\x0freloadable_type\x18\x04 \x02(\t\x12\x17\n\x0fmodel_data_path\x18\x05 \x02(\t\x12\x1a\n\x12runtime_thread_num\x18\x06 \x02(\x05\x12\x18\n\x10\x62\x61tch_infer_size\x18\x07 \x02(\x05\x12\x1a\n\x12\x65nable_batch_align\x18\x08 \x02(\x05\x12\x14\n\x0cversion_file\x18\t \x01(\t\x12\x14\n\x0cversion_type\x18\n \x01(\t\x12\x64\n\x19sparse_param_service_type\x18\x0b \x01(\x0e\x32\x41.baidu.paddle_serving.configure.EngineDesc.SparseParamServiceType\x12\'\n\x1fsparse_param_service_table_name\x18\x0c \x01(\t\x12\"\n\x1a\x65nable_memory_optimization\x18\r \x01(\x08\x12\x1b\n\x13static_optimization\x18\x0e \x01(\x08\x12!\n\x19\x66orce_update_static_cache\x18\x0f \x01(\x08\x12\x1e\n\x16\x65nable_ir_optimization\x18\x10 \x01(\x08\"9\n\x16SparseParamServiceType\x12\x08\n\x04NONE\x10\x00\x12\t\n\x05LOCAL\x10\x01\x12\n\n\x06REMOTE\x10\x02\"O\n\x10ModelToolkitConf\x12;\n\x07\x65ngines\x18\x01 \x03(\x0b\x32*.baidu.paddle_serving.configure.EngineDesc\"\xcb\x01\n\x0cResourceConf\x12\x1a\n\x12model_toolkit_path\x18\x01 \x02(\t\x12\x1a\n\x12model_toolkit_file\x18\x02 \x02(\t\x12\x1a\n\x12general_model_path\x18\x03 \x01(\t\x12\x1a\n\x12general_model_file\x18\x04 \x01(\t\x12\x18\n\x10\x63ube_config_path\x18\x05 \x01(\t\x12\x18\n\x10\x63ube_config_file\x18\x06 \x01(\t\x12\x17\n\x0f\x63ube_quant_bits\x18\x07 \x01(\x05\"/\n\x11\x44\x41GNodeDependency\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x0c\n\x04mode\x18\x02 \x02(\t\"n\n\x07\x44\x41GNode\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x0c\n\x04type\x18\x02 \x02(\t\x12G\n\x0c\x64\x65pendencies\x18\x03 \x03(\x0b\x32\x31.baidu.paddle_serving.configure.DAGNodeDependency\"g\n\x08Workflow\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x15\n\rworkflow_type\x18\x02 \x02(\t\x12\x36\n\x05nodes\x18\x03 \x03(\x0b\x32\'.baidu.paddle_serving.configure.DAGNode\"K\n\x0cWorkflowConf\x12;\n\tworkflows\x18\x01 \x03(\x0b\x32(.baidu.paddle_serving.configure.Workflow\"D\n\x13ValueMappedWorkflow\x12\x1b\n\x13request_field_value\x18\x01 \x02(\t\x12\x10\n\x08workflow\x18\x02 \x02(\t\"\xde\x01\n\x0cInferService\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x0e\n\x06merger\x18\x02 \x01(\t\x12-\n\x1e\x65nable_map_request_to_workflow\x18\x03 \x01(\x08:\x05\x66\x61lse\x12\x19\n\x11request_field_key\x18\x04 \x01(\t\x12S\n\x16value_mapped_workflows\x18\x05 \x03(\x0b\x32\x33.baidu.paddle_serving.configure.ValueMappedWorkflow\x12\x11\n\tworkflows\x18\x06 \x03(\t\"`\n\x10InferServiceConf\x12\x0c\n\x04port\x18\x01 \x01(\r\x12>\n\x08services\x18\x02 \x03(\x0b\x32,.baidu.paddle_serving.configure.InferService')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_ENGINEDESC_SPARSEPARAMSERVICETYPE = _descriptor.EnumDescriptor(
  name='SparseParamServiceType',
  full_name='baidu.paddle_serving.configure.EngineDesc.SparseParamServiceType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NONE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LOCAL', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REMOTE', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=577,
  serialized_end=634,
)
_sym_db.RegisterEnumDescriptor(_ENGINEDESC_SPARSEPARAMSERVICETYPE)


_ENGINEDESC = _descriptor.Descriptor(
  name='EngineDesc',
  full_name='baidu.paddle_serving.configure.EngineDesc',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='baidu.paddle_serving.configure.EngineDesc.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='type', full_name='baidu.paddle_serving.configure.EngineDesc.type', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='reloadable_meta', full_name='baidu.paddle_serving.configure.EngineDesc.reloadable_meta', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='reloadable_type', full_name='baidu.paddle_serving.configure.EngineDesc.reloadable_type', index=3,
      number=4, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='model_data_path', full_name='baidu.paddle_serving.configure.EngineDesc.model_data_path', index=4,
      number=5, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='runtime_thread_num', full_name='baidu.paddle_serving.configure.EngineDesc.runtime_thread_num', index=5,
      number=6, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='batch_infer_size', full_name='baidu.paddle_serving.configure.EngineDesc.batch_infer_size', index=6,
      number=7, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='enable_batch_align', full_name='baidu.paddle_serving.configure.EngineDesc.enable_batch_align', index=7,
      number=8, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='version_file', full_name='baidu.paddle_serving.configure.EngineDesc.version_file', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='version_type', full_name='baidu.paddle_serving.configure.EngineDesc.version_type', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sparse_param_service_type', full_name='baidu.paddle_serving.configure.EngineDesc.sparse_param_service_type', index=10,
      number=11, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sparse_param_service_table_name', full_name='baidu.paddle_serving.configure.EngineDesc.sparse_param_service_table_name', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='enable_memory_optimization', full_name='baidu.paddle_serving.configure.EngineDesc.enable_memory_optimization', index=12,
      number=13, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='static_optimization', full_name='baidu.paddle_serving.configure.EngineDesc.static_optimization', index=13,
      number=14, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='force_update_static_cache', full_name='baidu.paddle_serving.configure.EngineDesc.force_update_static_cache', index=14,
      number=15, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='enable_ir_optimization', full_name='baidu.paddle_serving.configure.EngineDesc.enable_ir_optimization', index=15,
      number=16, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ENGINEDESC_SPARSEPARAMSERVICETYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=59,
  serialized_end=634,
)


_MODELTOOLKITCONF = _descriptor.Descriptor(
  name='ModelToolkitConf',
  full_name='baidu.paddle_serving.configure.ModelToolkitConf',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='engines', full_name='baidu.paddle_serving.configure.ModelToolkitConf.engines', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=636,
  serialized_end=715,
)


_RESOURCECONF = _descriptor.Descriptor(
  name='ResourceConf',
  full_name='baidu.paddle_serving.configure.ResourceConf',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='model_toolkit_path', full_name='baidu.paddle_serving.configure.ResourceConf.model_toolkit_path', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='model_toolkit_file', full_name='baidu.paddle_serving.configure.ResourceConf.model_toolkit_file', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='general_model_path', full_name='baidu.paddle_serving.configure.ResourceConf.general_model_path', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='general_model_file', full_name='baidu.paddle_serving.configure.ResourceConf.general_model_file', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cube_config_path', full_name='baidu.paddle_serving.configure.ResourceConf.cube_config_path', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cube_config_file', full_name='baidu.paddle_serving.configure.ResourceConf.cube_config_file', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cube_quant_bits', full_name='baidu.paddle_serving.configure.ResourceConf.cube_quant_bits', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=718,
  serialized_end=921,
)


_DAGNODEDEPENDENCY = _descriptor.Descriptor(
  name='DAGNodeDependency',
  full_name='baidu.paddle_serving.configure.DAGNodeDependency',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='baidu.paddle_serving.configure.DAGNodeDependency.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mode', full_name='baidu.paddle_serving.configure.DAGNodeDependency.mode', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=923,
  serialized_end=970,
)


_DAGNODE = _descriptor.Descriptor(
  name='DAGNode',
  full_name='baidu.paddle_serving.configure.DAGNode',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='baidu.paddle_serving.configure.DAGNode.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='type', full_name='baidu.paddle_serving.configure.DAGNode.type', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dependencies', full_name='baidu.paddle_serving.configure.DAGNode.dependencies', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=972,
  serialized_end=1082,
)


_WORKFLOW = _descriptor.Descriptor(
  name='Workflow',
  full_name='baidu.paddle_serving.configure.Workflow',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='baidu.paddle_serving.configure.Workflow.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='workflow_type', full_name='baidu.paddle_serving.configure.Workflow.workflow_type', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='nodes', full_name='baidu.paddle_serving.configure.Workflow.nodes', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1084,
  serialized_end=1187,
)


_WORKFLOWCONF = _descriptor.Descriptor(
  name='WorkflowConf',
  full_name='baidu.paddle_serving.configure.WorkflowConf',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='workflows', full_name='baidu.paddle_serving.configure.WorkflowConf.workflows', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1189,
  serialized_end=1264,
)


_VALUEMAPPEDWORKFLOW = _descriptor.Descriptor(
  name='ValueMappedWorkflow',
  full_name='baidu.paddle_serving.configure.ValueMappedWorkflow',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='request_field_value', full_name='baidu.paddle_serving.configure.ValueMappedWorkflow.request_field_value', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='workflow', full_name='baidu.paddle_serving.configure.ValueMappedWorkflow.workflow', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1266,
  serialized_end=1334,
)


_INFERSERVICE = _descriptor.Descriptor(
  name='InferService',
  full_name='baidu.paddle_serving.configure.InferService',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='baidu.paddle_serving.configure.InferService.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='merger', full_name='baidu.paddle_serving.configure.InferService.merger', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='enable_map_request_to_workflow', full_name='baidu.paddle_serving.configure.InferService.enable_map_request_to_workflow', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='request_field_key', full_name='baidu.paddle_serving.configure.InferService.request_field_key', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value_mapped_workflows', full_name='baidu.paddle_serving.configure.InferService.value_mapped_workflows', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='workflows', full_name='baidu.paddle_serving.configure.InferService.workflows', index=5,
      number=6, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1337,
  serialized_end=1559,
)


_INFERSERVICECONF = _descriptor.Descriptor(
  name='InferServiceConf',
  full_name='baidu.paddle_serving.configure.InferServiceConf',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='port', full_name='baidu.paddle_serving.configure.InferServiceConf.port', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='services', full_name='baidu.paddle_serving.configure.InferServiceConf.services', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1561,
  serialized_end=1657,
)

_ENGINEDESC.fields_by_name['sparse_param_service_type'].enum_type = _ENGINEDESC_SPARSEPARAMSERVICETYPE
_ENGINEDESC_SPARSEPARAMSERVICETYPE.containing_type = _ENGINEDESC
_MODELTOOLKITCONF.fields_by_name['engines'].message_type = _ENGINEDESC
_DAGNODE.fields_by_name['dependencies'].message_type = _DAGNODEDEPENDENCY
_WORKFLOW.fields_by_name['nodes'].message_type = _DAGNODE
_WORKFLOWCONF.fields_by_name['workflows'].message_type = _WORKFLOW
_INFERSERVICE.fields_by_name['value_mapped_workflows'].message_type = _VALUEMAPPEDWORKFLOW
_INFERSERVICECONF.fields_by_name['services'].message_type = _INFERSERVICE
DESCRIPTOR.message_types_by_name['EngineDesc'] = _ENGINEDESC
DESCRIPTOR.message_types_by_name['ModelToolkitConf'] = _MODELTOOLKITCONF
DESCRIPTOR.message_types_by_name['ResourceConf'] = _RESOURCECONF
DESCRIPTOR.message_types_by_name['DAGNodeDependency'] = _DAGNODEDEPENDENCY
DESCRIPTOR.message_types_by_name['DAGNode'] = _DAGNODE
DESCRIPTOR.message_types_by_name['Workflow'] = _WORKFLOW
DESCRIPTOR.message_types_by_name['WorkflowConf'] = _WORKFLOWCONF
DESCRIPTOR.message_types_by_name['ValueMappedWorkflow'] = _VALUEMAPPEDWORKFLOW
DESCRIPTOR.message_types_by_name['InferService'] = _INFERSERVICE
DESCRIPTOR.message_types_by_name['InferServiceConf'] = _INFERSERVICECONF

EngineDesc = _reflection.GeneratedProtocolMessageType('EngineDesc', (_message.Message,), dict(
  DESCRIPTOR = _ENGINEDESC,
  __module__ = 'server_configure_pb2'
  # @@protoc_insertion_point(class_scope:baidu.paddle_serving.configure.EngineDesc)
  ))
_sym_db.RegisterMessage(EngineDesc)

ModelToolkitConf = _reflection.GeneratedProtocolMessageType('ModelToolkitConf', (_message.Message,), dict(
  DESCRIPTOR = _MODELTOOLKITCONF,
  __module__ = 'server_configure_pb2'
  # @@protoc_insertion_point(class_scope:baidu.paddle_serving.configure.ModelToolkitConf)
  ))
_sym_db.RegisterMessage(ModelToolkitConf)

ResourceConf = _reflection.GeneratedProtocolMessageType('ResourceConf', (_message.Message,), dict(
  DESCRIPTOR = _RESOURCECONF,
  __module__ = 'server_configure_pb2'
  # @@protoc_insertion_point(class_scope:baidu.paddle_serving.configure.ResourceConf)
  ))
_sym_db.RegisterMessage(ResourceConf)

DAGNodeDependency = _reflection.GeneratedProtocolMessageType('DAGNodeDependency', (_message.Message,), dict(
  DESCRIPTOR = _DAGNODEDEPENDENCY,
  __module__ = 'server_configure_pb2'
  # @@protoc_insertion_point(class_scope:baidu.paddle_serving.configure.DAGNodeDependency)
  ))
_sym_db.RegisterMessage(DAGNodeDependency)

DAGNode = _reflection.GeneratedProtocolMessageType('DAGNode', (_message.Message,), dict(
  DESCRIPTOR = _DAGNODE,
  __module__ = 'server_configure_pb2'
  # @@protoc_insertion_point(class_scope:baidu.paddle_serving.configure.DAGNode)
  ))
_sym_db.RegisterMessage(DAGNode)

Workflow = _reflection.GeneratedProtocolMessageType('Workflow', (_message.Message,), dict(
  DESCRIPTOR = _WORKFLOW,
  __module__ = 'server_configure_pb2'
  # @@protoc_insertion_point(class_scope:baidu.paddle_serving.configure.Workflow)
  ))
_sym_db.RegisterMessage(Workflow)

WorkflowConf = _reflection.GeneratedProtocolMessageType('WorkflowConf', (_message.Message,), dict(
  DESCRIPTOR = _WORKFLOWCONF,
  __module__ = 'server_configure_pb2'
  # @@protoc_insertion_point(class_scope:baidu.paddle_serving.configure.WorkflowConf)
  ))
_sym_db.RegisterMessage(WorkflowConf)

ValueMappedWorkflow = _reflection.GeneratedProtocolMessageType('ValueMappedWorkflow', (_message.Message,), dict(
  DESCRIPTOR = _VALUEMAPPEDWORKFLOW,
  __module__ = 'server_configure_pb2'
  # @@protoc_insertion_point(class_scope:baidu.paddle_serving.configure.ValueMappedWorkflow)
  ))
_sym_db.RegisterMessage(ValueMappedWorkflow)

InferService = _reflection.GeneratedProtocolMessageType('InferService', (_message.Message,), dict(
  DESCRIPTOR = _INFERSERVICE,
  __module__ = 'server_configure_pb2'
  # @@protoc_insertion_point(class_scope:baidu.paddle_serving.configure.InferService)
  ))
_sym_db.RegisterMessage(InferService)

InferServiceConf = _reflection.GeneratedProtocolMessageType('InferServiceConf', (_message.Message,), dict(
  DESCRIPTOR = _INFERSERVICECONF,
  __module__ = 'server_configure_pb2'
  # @@protoc_insertion_point(class_scope:baidu.paddle_serving.configure.InferServiceConf)
  ))
_sym_db.RegisterMessage(InferServiceConf)


# @@protoc_insertion_point(module_scope)
