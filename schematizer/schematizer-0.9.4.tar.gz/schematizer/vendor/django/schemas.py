from schematizer.schemas.base import BaseSchema


class Manager(BaseSchema):
    def __init__(self, schema):
        super().__init__()
        self.schema = schema

    def to_primitive(self, obj):
        return [self.schema.to_primitive(item) for item in obj.all()]
