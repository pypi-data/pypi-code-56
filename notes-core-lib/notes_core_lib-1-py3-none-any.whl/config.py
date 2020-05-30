import json
import pkg_resources


def config():
    path = 'config.json'
    filepath = pkg_resources.resource_filename(__name__, path)
    with open(filepath) as f:
        conf = json.load(f)

    return conf

def load(path):
    with open(path) as f:
        conf = json.load(f)

    return conf
