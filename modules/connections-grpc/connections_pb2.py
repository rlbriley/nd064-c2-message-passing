# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: connections.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11\x63onnections.proto\"\x8f\x03\n\x0e\x43onnectionList\x12\x32\n\x0b\x63onnections\x18\x01 \x03(\x0b\x32\x1d.ConnectionList.ConnectionMsg\x1a\xc8\x02\n\rConnectionMsg\x12;\n\x08location\x18\x01 \x01(\x0b\x32).ConnectionList.ConnectionMsg.LocationMsg\x12\x37\n\x06person\x18\x02 \x01(\x0b\x32\'.ConnectionList.ConnectionMsg.PersonMsg\x1aT\n\tPersonMsg\x12\n\n\x02id\x18\x01 \x01(\r\x12\x12\n\nfirst_name\x18\x02 \x01(\t\x12\x11\n\tlast_name\x18\x03 \x01(\t\x12\x14\n\x0c\x63ompany_name\x18\x04 \x01(\t\x1ak\n\x0bLocationMsg\x12\n\n\x02id\x18\x01 \x01(\r\x12\x11\n\tperson_id\x18\x02 \x01(\r\x12\x12\n\ncoordinate\x18\x03 \x01(\t\x12\x15\n\rcreation_time\x18\x05 \x01(\t\x12\x12\n\n_wkt_shape\x18\x06 \x01(\t\"\x91\x01\n\x0f\x43onnectionQuery\x12\x0e\n\x06person\x18\x01 \x01(\r\x12\x17\n\nstart_date\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x15\n\x08\x65nd_date\x18\x03 \x01(\tH\x01\x88\x01\x01\x12\x15\n\x08\x64istance\x18\x04 \x01(\rH\x02\x88\x01\x01\x42\r\n\x0b_start_dateB\x0b\n\t_end_dateB\x0b\n\t_distance2J\n\x12\x43onnectionsService\x12\x34\n\x0fperson_contacts\x12\x10.ConnectionQuery\x1a\x0f.ConnectionListb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'connections_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CONNECTIONLIST._serialized_start=22
  _CONNECTIONLIST._serialized_end=421
  _CONNECTIONLIST_CONNECTIONMSG._serialized_start=93
  _CONNECTIONLIST_CONNECTIONMSG._serialized_end=421
  _CONNECTIONLIST_CONNECTIONMSG_PERSONMSG._serialized_start=228
  _CONNECTIONLIST_CONNECTIONMSG_PERSONMSG._serialized_end=312
  _CONNECTIONLIST_CONNECTIONMSG_LOCATIONMSG._serialized_start=314
  _CONNECTIONLIST_CONNECTIONMSG_LOCATIONMSG._serialized_end=421
  _CONNECTIONQUERY._serialized_start=424
  _CONNECTIONQUERY._serialized_end=569
  _CONNECTIONSSERVICE._serialized_start=571
  _CONNECTIONSSERVICE._serialized_end=645
# @@protoc_insertion_point(module_scope)
