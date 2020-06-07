import os

from dagger.DaggerAPI import DaggerAPI
from dagger.integrations.aws_lambda import init as initLambda, isLambda
import dagger.integrations.aws_ecs

def initDagger(api_key, auto_initialize=True):
    api = DaggerAPI(api_key)

    if auto_initialize:
        if isLambda():
            initLambda(api)

    return api
