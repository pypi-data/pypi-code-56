from .models.publisher import Publisher
import ruamel.yaml
import sys

class ServiceConfigParser(object):

    def __init__(self, file_path):
        pass
        # yaml = ruamel.yaml.YAML()
        # yaml.register_class(Publisher)
        # with open(file_path, 'r') as file:
        #     loaded = yaml.load(file)
        #     p = Publisher.from_yaml(loaded['publisher'])
        #
        #     print(loaded)



        # yaml.dump([Publisher('Anthon', '18')], sys.stdout)
