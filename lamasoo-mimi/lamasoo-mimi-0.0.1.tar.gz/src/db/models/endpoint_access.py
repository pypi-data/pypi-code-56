
from elasticsearch_dsl import Document, Text, Date, Object, Integer, Nested
from datetime import datetime
from random_string import generate_random_code


class AccessLogElementIndex(Document):

    entity_type = Text()
    entity = Object(required=True)
    created_at = Date(default_timezone='UTC')


class EndpointAccessIndex(Document):
    crs_client_id = Object(required=True)
    track_id = Text(required=True)
    created_at = Date(default_timezone='UTC')

    access_log_elements = Nested(AccessLogElementIndex)

    class Meta:
        index = 'endpoint-access-index'

    def save(self, using=None, index=None, validate=True, skip_empty=True, **kwargs):
        clean_data = kwargs
        clean_data.update({'track_id': generate_random_code(30), 'created_at': str(datetime.now())})
        super().save(clean_data)
