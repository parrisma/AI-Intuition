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




DESCRIPTOR = _descriptor.FileDescriptor(
  name='pb_message1.proto',
  package='journey11.test.kpubsub',
  syntax='proto3',
  serialized_pb=_b('\n\x11pb_message1.proto\x12\x16journey11.test.kpubsub\".\n\nPBMessage1\x12\x0f\n\x07_field1\x18\x01 \x01(\t\x12\x0f\n\x07_field2\x18\x02 \x01(\x03\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_PBMESSAGE1 = _descriptor.Descriptor(
  name='PBMessage1',
  full_name='journey11.test.kpubsub.PBMessage1',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='_field1', full_name='journey11.test.kpubsub.PBMessage1._field1', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='_field2', full_name='journey11.test.kpubsub.PBMessage1._field2', index=1,
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
  serialized_start=45,
  serialized_end=91,
)

DESCRIPTOR.message_types_by_name['PBMessage1'] = _PBMESSAGE1

PBMessage1 = _reflection.GeneratedProtocolMessageType('PBMessage1', (_message.Message,), dict(
  DESCRIPTOR = _PBMESSAGE1,
  __module__ = 'pb_message1_pb2'
  # @@protoc_insertion_point(class_scope:journey11.test.kpubsub.PBMessage1)
  ))
_sym_db.RegisterMessage(PBMessage1)


# @@protoc_insertion_point(module_scope)
