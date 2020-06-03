from elasticsearch_dsl.connections import connections


def get_connection():
    connection = connections.get_connection('main_connection')
    if connection is None:
        connection = connections.create_connection(alias='main_connection', hosts=['http://192.168.100.30:9200'],
                                                   timeout=20, username='elastic', password='changeme')
    return connection
