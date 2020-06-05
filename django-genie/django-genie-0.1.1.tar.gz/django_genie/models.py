from django.apps import apps
from django.utils.text import camel_case_to_spaces


def get_field_names(fields):
    return ", ".join(["'{}'".format(x.name) for x in fields])


class Model:
    """A wrapper of the app's Model class. It has methods that make it easier to get model fields.
    This class receives a Model django db class.
    """
    def __init__(self, model):
        self.model = model

    @property
    def name(self):
        """Original model name. Just like the class."""
        return self.model._meta.object_name

    @property
    def field_names(self):
        """A list of all forward field names on the model and its parents,
        excluding ManyToManyFields.
        """
        return get_field_names(self.model._meta.fields)

    @property
    def local_field_names(self):
        """A list of field names on the model.
        """
        return get_field_names(self.model._meta.local_fields)

    @property
    def concrete_field_names(self):
        """A list of all concrete field names on the model and its parents."""
        return get_field_names(self.model._meta.concrete_fields)

    @property
    def serializer_field_names(self):
        """Serializers fields for serializers template"""
        return ", ".join([
            "'{}'".format(x.name) for x in self.model._meta.fields if
            x.name not in ["created_at", "updated_at", "deleted_at"]
        ])

    @property
    def admin_field_names(self):
        """Admin fields for admin template"""
        return ", ".join([
            "'{}'".format(x.name) for x in self.model._meta.fields if
            x.name not in ["id", "created_at", "updated_at", "deleted_at", "created_by", "updated_by"]
        ])

    @property
    def snake_case_name(self):
        """Model name in snake case."""
        return camel_case_to_spaces(self.name).replace(' ', '_')

    def __str__(self):
        return self.name


class Models:
    """List of all the models in the app"""

    def __init__(self, app):
        self.app = app
        self.models = [Model(model) for model in apps.get_app_config(self.app).get_models()]
