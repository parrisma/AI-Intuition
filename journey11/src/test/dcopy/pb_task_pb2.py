# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pb_task.proto

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
  name='pb_task.proto',
  package='journey11.experiment.proto_kafka',
  syntax='proto3',
  serialized_pb=_b('\n\rpb_task.proto\x12 journey11.experiment.proto_kafka\".\n\x06PBTask\x12\x12\n\n_task_name\x18\x01 \x01(\t\x12\x10\n\x08_task_id\x18\x02 \x01(\x03\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_PBTASK = _descriptor.Descriptor(
  name='PBTask',
  full_name='journey11.experiment.proto_kafka.PBTask',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='_task_name', full_name='journey11.experiment.proto_kafka.PBTask._task_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='_task_id', full_name='journey11.experiment.proto_kafka.PBTask._task_id', index=1,
      number=2, type=3, cpp_type=2, label=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=51,
  serialized_end=97,
)

DESCRIPTOR.message_types_by_name['PBTask'] = _PBTASK

PBTask = _reflection.GeneratedProtocolMessageType('PBTask', (_message.Message,), dict(
  DESCRIPTOR = _PBTASK,
  __module__ = 'pb_task_pb2'
  # @@protoc_insertion_point(class_scope:journey11.experiment.proto_kafka.PBTask)
  ))
_sym_db.RegisterMessage(PBTask)


# @@protoc_insertion_point(module_scope)
