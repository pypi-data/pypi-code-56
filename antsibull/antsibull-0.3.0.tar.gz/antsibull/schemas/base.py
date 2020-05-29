# coding: utf-8
# Author: Toshio Kuratomi <tkuratom@redhat.com>
# License: GPLv3+
# Copyright: Ansible Project, 2020

# Ignore Unitialized attribute errors because BaseModel works some magic
# to initialize the attributes when data is loaded into them.
# pyre-ignore-all-errors[13]
"""
Base schemas and supporting validator functions.

`Pydantic <https://pydantic-docs.helpmanual.io/>`_  is written to be an advanced version of
:python:mod:`dataclasses`.  It's primary use case is creating Python objects that hold data (think
of traditional C-style ``structs``).  As such, it is optimized for a slightly different use case
than what we are using it for.  However, the utility methods that come with pydantic make it quite
usable for data validation and normalization even with this difference in goals.

How to use these schemas effectively
====================================

The schemas shipped with antsibull allow you to validate and normalize plugin documentation.  This
way, you can use data from the plugins for web documentation, display on the command line, or
testing that your documentation is well formed.

To use these schemas, follow these steps:

* Choose the Schema that matches with the level of data that you want to validate and normalize.

    * If you want to validate and normalize :ansible:cmd:`ansible-doc` output, use the schemas in
      :mod:`antsibull.schemas.ansible_doc`.

      * :obj:`~antsibull.schemas.ansible_doc.AnsibleDocSchema` lets you validate the documentation
        for multiple plugins at once.  It is useful if all you want to do is validate documentation
        as you can run it once and then get all the errors.

      * If you want to normalize the data and use it to make documentation then the schemas in
        :attr:`~antsibull.schemas.ansible_doc.ANSIBLE_DOC_SCHEMAS` might be more appropriate.
        These schemas can be run on individual plugin data.  The advantage of using them is that
        an error in documentation will only fail that one plugin, not all of them.

    * If you need more fine grained control, you can use the schemas in
      :mod:`antsibull.schemas.docs.DOCS_SCHEMAS`.  These schemas give you access to the individual
      components of a plugin's documentation, doc, example, metadata, and return.  That way you can
      create documentation if any one of these (or specific ones) can be normalized even if the
      others cannot.

* Use one of the pydantic.BaseModel `alternate constructors
  <https://pydantic-docs.helpmanual.io/usage/models/#helper-functions>`_
  to load the data into the Schema.  :ansible:cmd:`ansible-doc` output is json, for instance, so you
  can feed that directly to :meth:`ansible_doc.ModulePluginSchema.parse_raw` (or the same method on
  a different schema).  If you have to manipulate the data as a dict first, you can use
  :meth:`ansible_doc.ModulePluginSchema.parse_obj`.

* The Schema will validate and normalize the data as it is loaded.

* Call the `dict() <https://pydantic-docs.helpmanual.io/usage/exporting_models/#modeldict>`_
  method on the returned model to convert the data back into a dict so that you can use it with
  templating engines or modify the structure of the data.

One example of doing all this:

.. code-block:: pycon

    >>> import sh, jinja2
    >>> from antsibull.schemas import ansible_doc
    >>> template = jinja2.Template('{{ name }} -- {{ doc["short_description"] }}')
    >>> module_json = sh.ansible_doc('-t', 'module', '--json', 'yum').stdout
    >>> module_model = ansible_doc.ModulePluginSchema.parse_raw(module_json)
    >>> # Retrieve the data from the __root__ field of the dict representation:
    >>> module_dict = module_model.dict()['__root__']
    >>> for plugin_name, plugin_info in module_dict.items():
    >>>     out = template.render(name=plugin_name, doc=plugin_info['doc'])
    >>>     print(out)
    >>> # yum -- Manages packages with the I(yum) package manager

Writing good pydantic schemas
=============================

* If you encounter something that needs to allow a certain value for legacy reasons but you don't
  want people to do that in the future, put the desired behaviour into the model and put the
  unwanted behaviour into a validator.  This makes it so the json-schema that can be built from
  the model will encapsulate the desired behaviour so that when people check their documentation
  with that, they will get an error while the code using the pydantic validator directly will
  automatically correct the data.

* The corollary is that when the definition should be added to the json-schema (for instance,
  to make validation more strict), those should be added as part of the type information in
  the model.

An example of both of the above:

.. code-block:: python

      class Model(BaseModel):
          new_name: str
          # Use pydantic.constr so that json-schema validations will also need to match the regex
          type: constr(regex='^(int|str|float)$')

          # Use validator on a specific attribute to change the value of the attribute
          @validator('type', pre=True)
          def fix_alternate_type_names(cls, value):
              '''These type names are commonly typoed.'''
              if value == 'string':
                  return 'str'
              if value == 'integer':
                  return 'int'
              return value

          # Use a root_validator to rename an attribute name to something else
          @root_validator(pre=True)
          def handle_renamed_attribute(cls, values):
              '''Rename an attribute to a new name.'''
              old_name = values.get('old_name')
              if old_name:
                  if values.get('new_name'):
                      raise ValueError('Only use `new_name`, not `old_name`.')
                  values['new_name'] = old_name
                  del values['old_name']
              return values

"""
import typing as t
from collections.abc import Mapping

import pydantic as p
import yaml

_SENTINEL = object()


#: Python scalars that are represented in JSON
JSONScalarT = t.Union[None, int, float, str]

#: Python types represented in JSON.  Unfortunately, we can't define this recursively yet.
JSONValueT = t.Union[JSONScalarT, t.List[t.Any], t.Dict[str, t.Any]]

#: Constrained string for valid Ansible environment variables
REQUIRED_ENV_VAR_F = p.Field(..., regex='[A-Z_]+')

#: option types are a set of strings that represent the types handled by argspec.
OPTION_TYPE_F = p.Field('str', regex='^(bits|bool|bytes|dict|float|int|json|jsonarg|list'
                        '|path|raw|sid|str)$')

#: Constrained string type for version numbers
REQUIRED_VERSION_F = p.Field(..., regex='^([0-9][0-9.]+)$')

#: Constrained string listing the possible types of a return field
RETURN_TYPE_F = p.Field('str', regex='^(bool|complex|dict|float|int|list|str)$')


def list_from_scalars(obj):
    """
    Create a list if the obj is a select scalary object.

    obj must be int, str, float, or None to be converted to a list.  Note that None converts to
    the empty list, rather than a list with None as its sole element.

    :arg obj: The object to convert if necessary.
    :return: obj wrapped in a list or the list itself.
    """
    if isinstance(obj, (str, int, float)):
        return [obj]

    if obj is None:
        return []

    return obj


def transform_return_docs(obj):
    """
    Attempt to convert data to a dict using a known strategy otherwise return.

    :arg obj: The return doc field to try to normalize
    """
    if isinstance(obj, Mapping):
        return obj

    if obj is None:
        return {}

    if isinstance(obj, str):
        try:
            new_obj = yaml.safe_load(obj)
        except Exception:
            obj = {"": obj}
        else:
            if isinstance(obj, Mapping):
                obj = new_obj
        return obj

    raise ValueError('Return docs are not the correct type')


def normalize_option_type_names(obj):
    """Normalize common mispellings of type names."""
    if obj == 'boolean':
        return 'bool'

    if obj in ('integer', 'number'):
        return 'int'

    if obj in ('string', 'strings'):
        return 'str'

    if obj == 'dictionary':
        return 'dict'

    if obj == 'lists':
        return 'list'

    return obj


class LocalConfig:
    """Settings we want on all of our models."""

    extra = p.Extra.forbid


class BaseModel(p.BaseModel):
    """BaseModel that has our preferred default config."""

    # pydantic Config classes are pure datastructures with no builtin special data
    # pyre-ignore[15]
    Config = LocalConfig


class DeprecationSchema(BaseModel):
    """Schema for Deprecation Fields."""

    removed_in: str = REQUIRED_VERSION_F
    why: str
    alternative: str = ''

    @p.root_validator(pre=True)
    def rename_version(cls, values):
        """Make deprecations at this level match the toplevel name."""
        version = values.get('version', _SENTINEL)
        if version is not _SENTINEL:
            if values.get('removed_in'):
                raise ValueError('Cannot specify `version` if `removed_in`'
                                 ' has been specified.')

            values['removed_in'] = version
            del values['version']

        return values

    @p.root_validator(pre=True)
    def merge_typo_names(cls, values):
        alternatives = values.get('alternatives', _SENTINEL)

        if alternatives is not _SENTINEL:
            if values.get('alternative'):
                raise ValueError('Cannot specify `alternatives` if `alternative`'
                                 ' has been specified.')

            values['alternative'] = alternatives
            del values['alternatives']

        return values


class OptionsSchema(BaseModel):
    description: t.List[str]
    aliases: t.List[str] = []
    choices: t.List[t.Union[str, None]] = []
    default: JSONValueT = None
    deprecated: DeprecationSchema = p.Field({})
    elements: str = OPTION_TYPE_F
    required: bool = False
    type: str = OPTION_TYPE_F
    version_added: str = 'historical'

    @p.validator('aliases', 'description', 'choices', pre=True)
    def list_from_scalars(cls, obj):
        return list_from_scalars(obj)

    @p.validator('type', 'elements', pre=True)
    def normalize_option_type(cls, obj):
        return normalize_option_type_names(obj)

    @p.root_validator(pre=True)
    def get_rid_of_name(cls, values):
        """
        Remove name from this schema.

        ``name`` is redundant with ``description``.  If we did need a shorter description here for
        some reason, we should call it ``short_description`` to match the other parts of the schema.
        """
        if 'name' in values:
            del values['name']
        return values

    @p.root_validator(pre=True)
    def merge_typo_names(cls, values):
        element_type = values.get('element_type', _SENTINEL)

        if element_type is not _SENTINEL:
            if values.get('elements'):
                raise ValueError('Cannot specify `element_type` if `elements` has been specified.')

            values['elements'] = element_type
            del values['element_type']

        element = values.get('element', _SENTINEL)

        if element is not _SENTINEL:
            if values.get('elements'):
                raise ValueError('Cannot specify `element` if `elements` has been specified.')

            values['elements'] = element
            del values['element']

        return values


class SeeAlsoModSchema(BaseModel):
    module: str
    description: str = ""


class SeeAlsoRefSchema(BaseModel):
    description: str
    ref: str


class SeeAlsoLinkSchema(BaseModel):
    description: str
    link: str
    name: str


class DocSchema(BaseModel):
    description: t.List[str]
    name: str
    short_description: str
    author: t.List[str] = []
    deprecated: DeprecationSchema = p.Field({})
    extends_documentation_fragment: t.List[str] = []
    filename: str = ''
    notes: t.List[str] = []
    requirements: t.List[str] = []
    seealso: t.List[t.Union[SeeAlsoModSchema, SeeAlsoRefSchema, SeeAlsoLinkSchema]] = []
    todo: t.List[str] = []
    version_added: str = 'historical'

    @p.validator('author', 'description', 'extends_documentation_fragment', 'notes',
                 'requirements', 'todo', pre=True)
    def list_from_scalars(cls, obj):
        return list_from_scalars(obj)

    @p.root_validator(pre=True)
    def remove_plugin_type(cls, values):
        """
        Remove the plugin_type field from the doc.

        The caller should already know the plugin_type.

        If we decide to keep this, we need to figure out how to fill it in for every plugin; right
        now it's only set (manually) on inventory and shell.
        """
        if 'plugin_type' in values:
            del values['plugin_type']
        return values

    @p.root_validator(pre=True)
    def merge_plugin_names(cls, values):
        """
        Normalize the field which plugin names are in.

        Some plugin types are putting their names into fields named after the type of plugin.
        This makes it harder for code to make use of the data as it has to know what the plugin
        type is and then look up that field.  Standardize on a ``name`` field instead.
        """
        names = {}
        for name_field in ('become', 'cache', 'callback', 'cliconf', 'connection',
                           'httpapi', 'inventory', 'lookup', 'module', 'netconf',
                           'strategy', 'vars'):
            plugin_name = values.get(name_field, _SENTINEL)
            if plugin_name is not _SENTINEL:
                names[name_field] = plugin_name

        if names:
            if len(names) > 1:
                raise ValueError('Specified {0} but only one can be'
                                 ' specified.'.format(names.keys()))
            if values.get('name'):
                raise ValueError('Cannot specify {0} if `name` has been'
                                 '  specified.'.format(names.keys()))

            # This seems to be the best way to get key and value from a one-element dict
            for name_field, name_field_value in names.items():
                values['name'] = name_field_value
                del values[name_field]

        return values

    @p.root_validator(pre=True)
    def merge_typo_names(cls, values):
        cb_type = values.get('callback_type', _SENTINEL)

        if cb_type is not _SENTINEL:
            if values.get('type'):
                raise ValueError('Cannot specify `callback_type` if `type` has been specified.')

            values['type'] = cb_type
            del values['callback_type']

        note = values.get('note', _SENTINEL)

        if note is not _SENTINEL:
            if values.get('notes'):
                raise ValueError('Cannot specify `note` if `notes` has been specified.')

            values['notes'] = note
            del values['note']

        authors = values.get('authors', _SENTINEL)

        if authors is not _SENTINEL:
            if values.get('author'):
                raise ValueError('Cannot specify `authors` if `author` has been specified.')

            values['author'] = authors
            del values['authors']

        return values
