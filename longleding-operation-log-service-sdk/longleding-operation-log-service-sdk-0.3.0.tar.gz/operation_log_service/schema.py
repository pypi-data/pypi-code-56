# -*- coding: utf-8 -*-
from datetime import datetime

from google.protobuf.timestamp_pb2 import Timestamp
from marshmallow import EXCLUDE, Schema, fields, post_load

from .model import OperationLog, OperationLogPageList
from .operationLogService_pb2 import OperationLogMessage, GetOperationLogsRequest, GetOperationLogsResponse


# Pb datetime
class PbDateTimeField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        ct = value.ToDatetime().isoformat()
        return ct if ct != '1970-01-01T00:00:00' else None

    def _deserialize(self, value, attr, data, **kwargs):
        p = Timestamp()
        d = datetime.fromisoformat(value)
        p.FromDatetime(d)
        return p


# object schema
class OperationLogObjectSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    time = fields.DateTime(default=None, missing=None)
    topic = fields.Str(default="", missing="")
    source = fields.Str(default="", missing="")
    tags = fields.Dict(default={}, missing={})
    content = fields.Str(default="", missing="")

    @post_load
    def make_object(self, data, **kwargs):
        return OperationLog(**data)


class OperationLogPageListObjectSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    logs = fields.List(fields.Nested(OperationLogObjectSchema), default=[], missing=[])
    total = fields.Int(default=0, missing=0)

    @post_load
    def make_object(self, data, **kwargs):
        return OperationLogPageList(**data)


# pb schema
class OperationLogPbSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    time = PbDateTimeField(default=None, missing=None)
    topic = fields.Str(default="", missing="")
    source = fields.Str(default="", missing="")
    tags = fields.Dict(default={}, missing={})
    content = fields.Str(default="", missing="")

    @post_load
    def make_object(self, data, **kwargs):
        return OperationLogMessage(**data)


class ListOfStringField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value.value_in is None or value.value_in == "":
            return []
        return list(value.value_in)

    def _deserialize(self, value, attr, data, **kwargs):
        return GetOperationLogsRequest.ListOfString(value_in=value)


class GetOperationLogsRequestPbSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    start_time = PbDateTimeField(default=None, missing=None)
    end_time = PbDateTimeField(default=None, missing=None)
    offset = fields.Int(default=0, missing=0)
    limit = fields.Int(default=0, missing=0)
    reverse = fields.Bool(default=False, missing=False)
    topic_in = fields.List(fields.Str(), default=[], missing=[])
    source_in = fields.List(fields.Str(), default=[], missing=[])
    tag_contains = fields.Dict(keys=fields.Str(), values=ListOfStringField(), default={}, missing={})

    @post_load
    def make_object(self, data, **kwargs):
        return GetOperationLogsRequest(**data)


class OperationLogPageListPbSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    logs = fields.List(fields.Nested(OperationLogPbSchema), default=[], missing=[])
    total = fields.Int(default=0, missing=0)

    @post_load
    def make_object(self, data, **kwargs):
        return GetOperationLogsResponse(**data)
