import os

from dagger.DaggerAPI import DaggerAPI
from dagger.integrations.aws_lambda import init as initLambda

def initDagger(api_key, auto_initialize=True):
    api = DaggerAPI(api_key)

    if auto_initialize:
        if os.getenv('_HANDLER'):
            initLambda(api)

    return api
