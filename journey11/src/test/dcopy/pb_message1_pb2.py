# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pb_message1.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import pb_state_pb2 as pb__state__pb2
import pb_task_pb2 as pb__task__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='pb_message1.proto',
  package='journey11.experiment.proto_kafka',
  syntax='proto3',
  serialized_pb=_b('\n\x11pb_message1.proto\x12 journey11.experiment.proto_kafka\x1a\x0epb_state.proto\x1a\rpb_task.proto\"\x91\x01\n\nPBMessage1\x12\x0e\n\x06_field\x18\x01 \x01(\t\x12\x39\n\x06_state\x18\x02 \x01(\x0e\x32).journey11.experiment.proto_kafka.PBState\x12\x38\n\x06_tasks\x18\x03 \x03(\x0b\x32(.journey11.experiment.proto_kafka.PBTaskb\x06proto3')
  ,
  dependencies=[pb__state__pb2.DESCRIPTOR,pb__task__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_PBMESSAGE1 = _descriptor.Descriptor(
  name='PBMessage1',
  full_name='journey11.experiment.proto_kafka.PBMessage1',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='_field', full_name='journey11.experiment.proto_kafka.PBMessage1._field', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='_state', full_name='journey11.experiment.proto_kafka.PBMessage1._state', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='_tasks', full_name='journey11.experiment.proto_kafka.PBMessage1._tasks', index=2,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=87,
  serialized_end=232,
)

_PBMESSAGE1.fields_by_name['_state'].enum_type = pb__state__pb2._PBSTATE
_PBMESSAGE1.fields_by_name['_tasks'].message_type = pb__task__pb2._PBTASK
DESCRIPTOR.message_types_by_name['PBMessage1'] = _PBMESSAGE1

PBMessage1 = _reflection.GeneratedProtocolMessageType('PBMessage1', (_message.Message,), dict(
  DESCRIPTOR = _PBMESSAGE1,
  __module__ = 'pb_message1_pb2'
  # @@protoc_insertion_point(class_scope:journey11.experiment.proto_kafka.PBMessage1)
  ))
_sym_db.RegisterMessage(PBMessage1)


# @@protoc_insertion_point(module_scope)
