# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pb_l1.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import pb_l2_pb2 as pb__l2__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='pb_l1.proto',
  package='journey11.experiment.proto_kafka',
  syntax='proto3',
  serialized_pb=_b('\n\x0bpb_l1.proto\x12 journey11.experiment.proto_kafka\x1a\x0bpb_l2.proto\"O\n\x04PBL1\x12:\n\n_single_l2\x18\x01 \x01(\x0b\x32&.journey11.experiment.proto_kafka.PBL2\x12\x0b\n\x03_s1\x18\x02 \x01(\tb\x06proto3')
  ,
  dependencies=[pb__l2__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_PBL1 = _descriptor.Descriptor(
  name='PBL1',
  full_name='journey11.experiment.proto_kafka.PBL1',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='_single_l2', full_name='journey11.experiment.proto_kafka.PBL1._single_l2', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='_s1', full_name='journey11.experiment.proto_kafka.PBL1._s1', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=62,
  serialized_end=141,
)

_PBL1.fields_by_name['_single_l2'].message_type = pb__l2__pb2._PBL2
DESCRIPTOR.message_types_by_name['PBL1'] = _PBL1

PBL1 = _reflection.GeneratedProtocolMessageType('PBL1', (_message.Message,), dict(
  DESCRIPTOR = _PBL1,
  __module__ = 'pb_l1_pb2'
  # @@protoc_insertion_point(class_scope:journey11.experiment.proto_kafka.PBL1)
  ))
_sym_db.RegisterMessage(PBL1)


# @@protoc_insertion_point(module_scope)
