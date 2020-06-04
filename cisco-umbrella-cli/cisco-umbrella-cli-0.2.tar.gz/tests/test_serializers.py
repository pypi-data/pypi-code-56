"""
    This is the test suite for serializers and models of the Umbrella API.
"""

from unittest import mock

import pytest
from marshmallow import ValidationError


from umbrella_cli import serializers, models


class TestSiteSerializer:

    @pytest.fixture
    def single_site(self):
        return """{
            "originId": 385265878,
            "isDefault": false,
            "name": "Home Office",
            "modifiedAt": "2020-03-20T18:08:36.000Z",
            "createdAt": "2020-03-20T18:08:36.000Z",
            "type": "site",
            "internalNetworkCount": 2,
            "vaCount": 2,
            "siteId": 1334164
            }"""
    
    @pytest.fixture
    def multiple_sites(self):
        return """[{
                    "originId": 395218748,
                    "isDefault": false,
                    "name": "BLUE",
                    "modifiedAt": "2020-04-05T19:07:38.000Z",
                    "createdAt": "2020-04-05T19:07:38.000Z",
                    "type": "site",
                    "internalNetworkCount": 2,
                    "vaCount": 4,
                    "siteId": 1479824
                },
                {
                    "originId": 136056751,
                    "isDefault": true,
                    "name": "Default Site",
                    "modifiedAt": "2018-03-06T01:23:13.000Z",
                    "createdAt": "2018-03-06T01:23:13.000Z",
                    "type": "site",
                    "internalNetworkCount": 0,
                    "vaCount": 0,
                    "siteId": 635875
                }]"""

    def test_site_serialize_with_valid_single_object(self, single_site):
        """ Test a working serialization of a single object. """
        schema = serializers.SiteSerializer()
        result = schema.loads(single_site)

        assert isinstance(result, models.Site)
        assert isinstance(result.name, str)
        assert result.name == "Home Office"

        assert isinstance(result.va_count, int)
        assert result.va_count == 2

        assert isinstance(result.is_default, bool)
        assert result.is_default == False

        #! Python datetime not supporting Zulu timezone
        #assert isinstance(result['created_at'], dt.datetime)
        #assert isinstance(result['created_at'], dt.datetime(
        #    year=2020, month=4, day=5,
        #    hour=19, minute=7, second=38
        #    ))
    
    def test_site_serialize_with_valid_multiple_objects(self, multiple_sites):
        """ Test a working serialization of multiple objects. """
        schema = serializers.SiteSerializer(many=True)
        result = schema.loads(multiple_sites)

        assert len(result) == 2

    def test_site_serialize_raise_validation_error(self):
        """ Test a thrown exception by invalid data. """
        data = """{
            "originId": 385265878,
            "isDefault": false,
            "name": 2,
            "modifiedAt": "2020-03-20T18:08:36.000Z",
            "createdAt": "2020-03-20T18:08:36.000Z",
            "type": "site",
            "internalNetworkCount": "fake",
            "vaCount": 2,
            "siteId": 1334164
            }"""

        with pytest.raises(ValidationError):
            schema = serializers.SiteSerializer()
            schema.loads(data)

    def test_site_dump_for_new_object(self):
        """ Test a serializer dump with read-write fields only"""
        site = models.Site(name="Test")

        schema = serializers.SiteSerializer()
        result = schema.dump(site)

        assert result == {"name":"Test"}

    def test_site_dump_read_only_fields(self, single_site):
        """ Test a serializer dump with read_only fields """
        
        site = models.Site(
            origin_id=385265878,
            is_default=False,
            name="Home Office",
            modified_at="2020-03-20T18:08:36.000Z",
            created_at="2020-03-20T18:08:36.000Z",
            type="site",
            internal_network_count=2,
            va_count=2,
            site_id=1334164
            )
        schema = serializers.SiteSerializer()

        result = schema.dump(site)

        assert result == {"name": "Home Office"}


class TestInternalNetworkSerializer:
    """ Test cases for umbrella_cli.serializers.InternalNetworkSerializer """

    @pytest.fixture
    def serializer(self):
        return serializers.InternalNetworkSerializer

    @pytest.fixture
    def single_object(self):
        """ Returns a single object """
        return """{
        "originId": 396397650,
        "ipAddress": "10.1.200.0",
        "prefixLength": 24,
        "createdAt": "2020-04-08T02:51:34.000Z",
        "modifiedAt": "2020-04-08T02:51:34.000Z",
        "name": "RED",
        "siteId": 1479824,
        "siteName": ""}
        """    

    @pytest.fixture
    def multiple_objects(self):
        """ Return a list of objects """
        return """[
    {
        "originId": 396397504,
        "ipAddress": "10.1.100.0",
        "prefixLength": 24,
        "createdAt": "2020-04-08T02:51:00.000Z",
        "modifiedAt": "2020-04-08T02:51:00.000Z",
        "name": "BLUE",
        "siteId": 1479824,
        "siteName": ""
    },
    {
        "originId": 396397650,
        "ipAddress": "10.1.200.0",
        "prefixLength": 24,
        "createdAt": "2020-04-08T02:51:34.000Z",
        "modifiedAt": "2020-04-08T02:51:34.000Z",
        "name": "RED",
        "siteId": 1479824,
        "siteName": ""
    }]"""

    def test_internal_network_single_valid_load(self, single_object, serializer):
        """
        Test a single object getting serialized successfully
        """
        result = serializer().loads(single_object)

        assert isinstance(result, models.InternalNetwork)

        assert result.origin_id == 396397650
        assert result.name == "RED"
        assert result.ip_address == "10.1.200.0"
        assert result.prefix_length == 24
        assert result.created_at == "2020-04-08T02:51:34.000Z"
        assert result.modified_at == "2020-04-08T02:51:34.000Z"
        assert result.site_id == 1479824
        assert result.site_name == ""

    def test_internal_network_single_raise_exception(self, serializer):
        """
        Test a single object with wrong data types raising a ValidationError
        """
        data = """
            {
                "originId": "123",
                "name": 123
            }
        """

        with pytest.raises(ValidationError):
            serializer().loads(data)

    def test_internal_network_multiple_valid_load(self, multiple_objects, 
                                                  serializer):
        """
        Test multiple objects getting serialized successfully
        """
        result = serializer().loads(multiple_objects, many=True)

        assert len(result) == 2
        assert isinstance(result[0], models.InternalNetwork)
        assert isinstance(result[1], models.InternalNetwork)


    def test_internal_network_single_valid_dump(self, serializer):
        """
        Test the serialization of a model object.
        """
        instance = models.InternalNetwork(
            name="TEST",
            ip_address="192.0.2.0",
            prefix_length=24,
            network_id=123456,
            created_at="2020-04-08T02:51:34.000Z"
        )

        result = serializer().dump(instance)

        assert result == {
            "name": "TEST",
            "ipAddress": "192.0.2.0",
            "prefixLength": 24,
            "networkId": 123456
        }

    def test_internal_network_single_dump_raises_validation_error(
            self, serializer):
        """
        Test the serialization of a model object with wron
        """
        instance = models.InternalNetwork(
            name="TEST",
            ip_address="192.0.2.0",
            prefix_length="twenty-four"
        )

        with pytest.raises(ValueError):
            serializer().dump(instance)
