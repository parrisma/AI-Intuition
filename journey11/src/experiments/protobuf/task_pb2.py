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
  package='journey11',
  syntax='proto3',
  serialized_pb=_b('\n\npb_task.proto\x12\tjourney11\"*\n\x04Task\x12\x11\n\ttask_name\x18\x01 \x01(\t\x12\x0f\n\x07task_id\x18\x02 \x01(\x03\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_TASK = _descriptor.Descriptor(
  name='Task',
  full_name='journey11.Task',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_name', full_name='journey11.Task.task_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='task_id', full_name='journey11.Task.task_id', index=1,
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
  serialized_start=25,
  serialized_end=67,
)

DESCRIPTOR.message_types_by_name['Task'] = _TASK

Task = _reflection.GeneratedProtocolMessageType('Task', (_message.Message,), dict(
  DESCRIPTOR = _TASK,
  __module__ = 'task_pb2'
  # @@protoc_insertion_point(class_scope:journey11.Task)
  ))
_sym_db.RegisterMessage(Task)


# @@protoc_insertion_point(module_scope)
