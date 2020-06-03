from abc import ABC, abstractmethod
from jsonschema import validate
from jsonschema import exceptions


class ConfigChapter(ABC):
    validation_schema = ''

    @staticmethod
    @abstractmethod
    def from_yaml(input_dict):
        ConfigChapter.validate(input_dict)

    # @abstractmethod
    # def to_json(self):
    #     return NotImplemented

    # @abstractmethod
    @staticmethod
    def validate(self, received_chapter):
        try:
            return validate(received_chapter, schema=self.validation_schema)
        except exceptions.ValidationError as ex:
            print(ex)
            raise ex
