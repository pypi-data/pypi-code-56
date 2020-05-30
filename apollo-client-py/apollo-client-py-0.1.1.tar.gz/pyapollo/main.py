from .apollo_client import ApolloClient

client = ApolloClient(
    app_id='user-event-center', cluster='dev', 
    config_server_url='http://config.applooking.com/', 
    secret='adb1922402bb43e6a5dea3812b536893'
)
client.start()

client.get_value('MONGO_URI')