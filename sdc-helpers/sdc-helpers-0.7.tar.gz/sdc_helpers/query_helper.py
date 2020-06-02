"""
   SDC Query helper module
"""
import os
import json
import boto3
import pymysql
from sdc_helpers.redis_helper import RedisHelper

class QueryHelper:
    """
        Query helper class
    """
    db_conn = None
    cursor = None
    redis_helper = None

    def __init__(self, **kwargs):
        """
            Init a new QueryHelper obj
            kwargs:
                rds_config (dict) : config arguments for mysql connector
                redis_config (dict) : config arguments for redis connector
        """
        # get rds config
        rds_config = kwargs.get('rds_config', {})
        rds_host = rds_config.get('host', None)
        rds_user = rds_config.get('username', None)
        rds_password = rds_config.get('password', None)
        rds_port = rds_config.get('port', None)
        rds_db = rds_config.get('db', None)

        # get redis config
        redis_config = kwargs.get('redis_config', {})
        redis_host = redis_config.get('host', None)
        redis_port = redis_config.get('port', None)
        redis_db = redis_config.get('db', None)
        # temporary fix - these should be passed at init time
        if rds_host is None:
            rds_host = os.getenv('RDS_HOST', 'localhost')
        # temporary fix - these should be passed at init time
        if rds_user is None:
            rds_user = os.getenv('RDS_USERNAME', 'root')
        # temporary fix - these should be passed at init time
        if rds_password is None:
            rds_password = os.getenv('RDS_PASSWORD')
        # temporary fix - these should be passed at init time
        if rds_port is None:
            rds_port = int(os.getenv('RDS_PORT', '3306'))
        # temporary fix - these should be passed at init time
        if rds_db is None:
            rds_db = os.getenv('RDS_DB_NAME', 'sdc')
        try:
            self.db_conn = pymysql.connect(
                host=rds_host,
                user=rds_user,
                passwd=rds_password,
                db=rds_db,
                port=rds_port,
                connect_timeout=5,
                cursorclass=pymysql.cursors.DictCursor
            )

            self.cursor = self.db_conn.cursor()

        except pymysql.MySQLError as exception:
            print(exception)
        # instantiate a redis helper
        self.redis_helper = RedisHelper(host=redis_host, port=redis_port, db=redis_db)

    def __del__(self):
        self.db_conn.close()
        del self.redis_helper

    def get_clients(self) -> dict:
        """
            Get all the clients from the database

        return:
            clients (dict) : Returns all the clients from the database

        """
        self.cursor.execute('SELECT * FROM clients')

        return self.cursor.fetchall()

    def get_client(
            self,
            *,
            api_key_id: str = None,
            client_id: str = None,
            from_cache: bool = True
    ) -> dict:
        """
            Get the specified client from cache or database

            args:
                api_key_id (str): The AWS API Gateway API Key Id
                client_id (int): ID of the client in the database
                from_cache (bool): Retrieve the client from cache - Default True

            return:
                client (dict) : Returns the specified client

        """
        if not api_key_id and not client_id:
            raise Exception('ClientError: api_key_id or id is required for this function')

        if api_key_id and client_id:
            raise Exception(
                'ClientError: Only one of api_key_id or id should be specified for this function'
            )

        if api_key_id:
            client_redis_key = 'client-{api_key_id}'.format(api_key_id=api_key_id)
        else:
            client_redis_key = 'client-{client_id}'.format(client_id=client_id)

        client_redis = self.redis_helper.redis_get(key=client_redis_key)
        client = None

        if (
                not from_cache or
                not client_redis
        ):
            if api_key_id:
                client = boto3.client('apigateway')
                api_key = client.get_api_key(apiKey=api_key_id)

                if 'tags' not in api_key or 'client_code' not in api_key['tags']:
                    raise Exception(
                        ('ClientError: client_code not set up for this API key. '
                         'Please contact support'
                        )
                    )
                sql = (
                    "SELECT * FROM `clients` "
                    "WHERE `code` = %s AND "
                    "`deleted_at` IS NULL"
                )
                self.cursor.execute(sql, (api_key['tags']['client_code'], ))
            else:
                sql = (
                    "SELECT * FROM `clients` "
                    "WHERE `id` = %s AND "
                    "`deleted_at` IS NULL"
                )
                self.cursor.execute(sql, (client_id, ))

            client = self.cursor.fetchone()

            if client:
                self.redis_helper.redis_set(
                    key=client_redis_key,
                    value=json.dumps(client, default=str)
                )
        else:
            client = json.loads(client_redis)

        return client

    def get_services(self) -> dict:
        """
            Get all services from the database

            return:
                services (dict) : Returns all the services from the database

        """
        self.cursor.execute('SELECT * FROM services WHERE deleted_at IS NULL')

        return self.cursor.fetchall()

    def get_service(self, *, slug: str, from_cache: bool = True) -> dict:
        """
            Get the specified client from cache or database

            args:
                slug (str): slug of the service in the database
                from_cache (bool): Retrieve the service from cache - Default True

            return:
                service (dict) : Returns the specified service

        """
        service_redis_key = 'service-{slug}'.format(slug=slug)
        service_redis = self.redis_helper.redis_get(key=service_redis_key)
        service = None

        if (
                not from_cache or
                not service_redis
        ):
            sql = (
                "SELECT * FROM `services` "
                "WHERE `slug` = %s "
                "AND deleted_at IS NULL"
            )
            self.cursor.execute(sql, (slug, ))

            service = self.cursor.fetchone()

            if service:
                self.redis_helper.redis_set(
                    key=service_redis_key,
                    value=json.dumps(service, default=str)
                )
        else:
            service = json.loads(service_redis)

        return service

    def get_subscription_properties(
            self,
            *,
            client_id: int,
            service_id: int,
            from_cache: bool = True
    ) -> dict:
        """
            Get the specified subscription properties from cache or database

            args:
                client_id (id): client_id of the subscription in the database
                service_id (id): service_id of the subscription in the database
                from_cache (bool): Retrieve the service from cache - Default True

            return:
                properties (dict) : Returns the specified subscription's properties

        """
        subscription_properties_redis_key = ('subscription-properties-{client_id}-{service_id}'
                                             .format(client_id=client_id, service_id=service_id))
        subscription_properties_redis = self.redis_helper.redis_get(
            key=subscription_properties_redis_key
        )
        subscription_properties = None

        if (
                not from_cache or
                not subscription_properties_redis
        ):
            sql = (
                "SELECT `properties` FROM `subscriptions`"
                "WHERE `client_id` = %s AND "
                "`service_id` = %s AND "
                "`deleted_at` IS NULL AND "
                "`subscriptions`.`properties` IS NOT NULL"
            )
            self.cursor.execute(sql, (client_id, service_id))

            subscription = self.cursor.fetchone()
            subscription_properties = None

            if subscription:
                subscription_properties = json.loads(subscription['properties'])

                self.redis_helper.redis_set(
                    key=subscription_properties_redis_key,
                    value=json.dumps(subscription_properties, default=str)
                )
        else:
            subscription_properties = json.loads(subscription_properties_redis)

        return subscription_properties

    def get_subscriptions_properties(self, *, service_id: int) -> dict:
        """
            Get all the specified service's subscriptions properties from the database

            args:
                service_id (id): service_id of the subscription in the database

            return:
                properties (dict) : Returns the specified service's subscription's properties

        """
        sql = (
            "SELECT `clients`.`id`, "
            "`subscriptions`.`properties` "
            "FROM `subscriptions` "
            "LEFT JOIN `clients` ON `client_id` = `clients`.`id` "
            "WHERE `service_id` = %s AND "
            "`subscriptions`.`deleted_at` IS NULL AND "
            "`subscriptions`.`properties` IS NOT NULL"
        )

        self.cursor.execute(sql, (service_id, ))

        subscriptions = self.cursor.fetchall()

        properties = {}

        for subscription in subscriptions:
            properties[subscription['id']] = json.loads(subscription['properties'])

        return properties

    def update_subscription_properties(self, *, client_id: id, service_id: id, properties: str):
        """
            Update the specified subscription's properties in the database

            args:
                client_id (id): client_id of the subscription in the database
                service_id (id): service_id of the subscription in the database
                properties (str): The new properties to update with

        """
        sql = (
            "UPDATE `subscriptions` "
            "SET `properties` = %s, `updated_at` = NOW() "
            "WHERE `client_id` = %s AND `service_id` = %s"
        )

        self.cursor.execute(sql, (properties, client_id, service_id))

        self.db_conn.commit()

        subscription_properties_redis_key = ('subscription-properties-{client_id}-{service_id}'
                                             .format(client_id=client_id, service_id=service_id))

        self.redis_helper.redis_set(
            key=subscription_properties_redis_key,
            value=properties
        )
