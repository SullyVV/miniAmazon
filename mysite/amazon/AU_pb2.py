 # Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: AU.proto

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
  name='AU.proto',
  package='',
  syntax='proto2',
  serialized_pb=_b('\n\x08\x41U.proto\"\x82\x01\n\x02\x41U\x12\x0c\n\x04\x66lag\x18\x01 \x02(\x05\x12\x0e\n\x06shipid\x18\x02 \x02(\x05\x12\x0c\n\x04whid\x18\x03 \x02(\x05\x12\x11\n\tpackageid\x18\x04 \x01(\x03\x12\t\n\x01x\x18\x05 \x02(\x05\x12\t\n\x01y\x18\x06 \x02(\x05\x12\x0e\n\x06ups_id\x18\x07 \x01(\x05\x12\x17\n\x0f\x64\x65tailofpackage\x18\x08 \x01(\t\"(\n\x02UA\x12\x11\n\tpackageid\x18\x01 \x02(\x03\x12\x0f\n\x07truckid\x18\x02 \x02(\x05')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_AU = _descriptor.Descriptor(
  name='AU',
  full_name='AU',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='flag', full_name='AU.flag', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='shipid', full_name='AU.shipid', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='whid', full_name='AU.whid', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='packageid', full_name='AU.packageid', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='x', full_name='AU.x', index=4,
      number=5, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y', full_name='AU.y', index=5,
      number=6, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ups_id', full_name='AU.ups_id', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='detailofpackage', full_name='AU.detailofpackage', index=7,
      number=8, type=9, cpp_type=9, label=1,
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
  serialized_start=13,
  serialized_end=143,
)


_UA = _descriptor.Descriptor(
  name='UA',
  full_name='UA',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='packageid', full_name='UA.packageid', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='truckid', full_name='UA.truckid', index=1,
      number=2, type=5, cpp_type=1, label=2,
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
  serialized_start=145,
  serialized_end=185,
)

DESCRIPTOR.message_types_by_name['AU'] = _AU
DESCRIPTOR.message_types_by_name['UA'] = _UA

AU = _reflection.GeneratedProtocolMessageType('AU', (_message.Message,), dict(
  DESCRIPTOR = _AU,
  __module__ = 'AU_pb2'
  # @@protoc_insertion_point(class_scope:AU)
  ))
_sym_db.RegisterMessage(AU)

UA = _reflection.GeneratedProtocolMessageType('UA', (_message.Message,), dict(
  DESCRIPTOR = _UA,
  __module__ = 'AU_pb2'
  # @@protoc_insertion_point(class_scope:UA)
  ))
_sym_db.RegisterMessage(UA)


# @@protoc_insertion_point(module_scope)
