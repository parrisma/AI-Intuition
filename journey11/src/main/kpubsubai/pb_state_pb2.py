# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pb_state.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='pb_state.proto',
  package='journey11.kpubsubai',
  syntax='proto3',
  serialized_pb=_b('\n\x0epb_state.proto\x12\x13journey11.kpubsubai*Y\n\x07PBState\x12\x06\n\x02S0\x10\x00\x12\x06\n\x02S1\x10\x01\x12\x06\n\x02S2\x10\x02\x12\x06\n\x02S3\x10\x03\x12\x06\n\x02S4\x10\x04\x12\x06\n\x02S5\x10\x05\x12\x06\n\x02S6\x10\x06\x12\x06\n\x02S7\x10\x07\x12\x06\n\x02S8\x10\x08\x12\x06\n\x02S9\x10\tb\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

_PBSTATE = _descriptor.EnumDescriptor(
  name='PBState',
  full_name='journey11.kpubsubai.PBState',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='S0', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='S1', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='S2', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='S3', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='S4', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='S5', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='S6', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='S7', index=7, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='S8', index=8, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='S9', index=9, number=9,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=39,
  serialized_end=128,
)
_sym_db.RegisterEnumDescriptor(_PBSTATE)

PBState = enum_type_wrapper.EnumTypeWrapper(_PBSTATE)
S0 = 0
S1 = 1
S2 = 2
S3 = 3
S4 = 4
S5 = 5
S6 = 6
S7 = 7
S8 = 8
S9 = 9


DESCRIPTOR.enum_types_by_name['PBState'] = _PBSTATE


# @@protoc_insertion_point(module_scope)
