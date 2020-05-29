from .base import BaseModel
from . import fields


class Cluster(BaseModel):
    id = fields.StringField()
    name = fields.StringField()
    endpoint = fields.StringField()
    region = fields.StringField()
    version = fields.StringField()
    auto_upgrade = fields.BooleanField()
    ipv4 = fields.StringField()
    cluster_subnet = fields.StringField()
    service_subnet = fields.StringField()
    vpc_uuid = fields.StringField()
    # tags =
    # maintenance_policy =
    # node_pools =
    created_at = fields.StringField()
    updated_at = fields.StringField()
    # status =

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
