"""
    This module contains all the Schema objects for the Umbrella Management
    API to interact with the response object as Python native constructs. 
"""

from marshmallow import Schema, fields, post_load

from umbrella_cli import models

class BaseSerializer(Schema):
    _model = models.UmbrellaModel
    
    @post_load
    def post_load(self, data, **kwargs):
        return self._model(**data)


class SiteSerializer(BaseSerializer):
    """ Umbrella internal site serializer """
    _model = models.Site

    origin_id = fields.Integer(load_only=True, data_key="originId")
    name = fields.String(required=True)
    site_id = fields.Integer(load_only=True, data_key="siteId")
    is_default = fields.Boolean(load_only=True, data_key="isDefault")
    type = fields.String(load_only=True)
    internal_network_count = fields.Integer(
        load_only=True, data_key="internalNetworkCount"
        )
    va_count = fields.Integer(load_only=True, data_key="vaCount")

    #! Python datetime not supporting Zulu timezone
    #modified_at = fields.DateTime(
    #    format="YYYY-MM-DDTHH:MM:SS.fffZ", load_only=True, data_key="modifiedAt"
    #    )
    #created_at = fields.DateTime(
    #    format="YYYY-MM-DDTHH:MM:SS.fffZ", load_only=True, data_key="createdAt"
    #    )
    modified_at = fields.String(load_only=True, data_key="modifiedAt")
    created_at = fields.String(load_only=True, data_key="createdAt")


class InternalNetworkSerializer(BaseSerializer):
    """ Umbrella internal network serializer """
    _model = models.InternalNetwork

    origin_id = fields.Integer(load_only=True, data_key="originId")
    name = fields.String(required=True)
    ip_address = fields.String(required=True, data_key="ipAddress")
    prefix_length = fields.Integer(required=True, data_key="prefixLength")
    site_id = fields.Integer(data_key="siteId")
    site_name = fields.String(load_only=True, data_key="siteName")
    network_name = fields.String(load_only=True, data_key="networkName")
    network_id = fields.Integer(data_key="networkId")
    tunnel_name = fields.String(load_only=True, data_key="tunnelName")
    tunnel_id = fields.String(data_key="tunnelId")
    modified_at = fields.String(load_only=True, data_key="modifiedAt")
    created_at = fields.String(load_only=True, data_key="createdAt")