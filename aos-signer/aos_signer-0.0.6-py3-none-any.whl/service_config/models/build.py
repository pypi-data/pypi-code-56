from six import attr

from .config_chapter import ConfigChapter


class Build(ConfigChapter):
    schema = {
        "type": "object",
        "properties": {
        "price": {"type": "number"},
        "name": {"type": "string"},
        },
    }


    def from_yaml(self, input_dict):
        pass

    def to_json(self):
        pass

    def validate(self):
        pass

    # @attr.
    # def os(self):
    #     return


# build:
#     os: string
#     arch: string
#     sign_key: string
#     sign_certificate: string
#     remove_non_regular_files: bool, optional (default true)
#     context: string, optional