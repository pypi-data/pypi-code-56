from marshmallow import Schema, fields, post_dump, post_load
from splitiorequests.models.splits.split import Split
from splitiorequests.schemas.splits import tag_schema, traffic_type_schema


class SplitSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str()
    trafficType = fields.Nested(traffic_type_schema.TrafficTypeSchema)
    creationTime = fields.Integer()
    tags = fields.List(fields.Nested(tag_schema.TagSchema), missing=None)

    @post_load
    def load_split(self, data, **kwargs):
        return Split(**data)

    @post_dump
    def clean_empty(self, data, **kwargs):
        new_data = data.copy()
        for field_key in (key for key in data if data[key] is None and key != 'tags'):
            del new_data[field_key]
        return new_data
