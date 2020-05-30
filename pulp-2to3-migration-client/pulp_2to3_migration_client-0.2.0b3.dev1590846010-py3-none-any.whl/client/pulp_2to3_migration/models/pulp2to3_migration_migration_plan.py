# coding: utf-8

"""
    Pulp 3 API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from pulpcore.client.pulp_2to3_migration.configuration import Configuration


class Pulp2to3MigrationMigrationPlan(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'pulp_href': 'str',
        'pulp_created': 'datetime',
        'plan': 'object'
    }

    attribute_map = {
        'pulp_href': 'pulp_href',
        'pulp_created': 'pulp_created',
        'plan': 'plan'
    }

    def __init__(self, pulp_href=None, pulp_created=None, plan=None, local_vars_configuration=None):  # noqa: E501
        """Pulp2to3MigrationMigrationPlan - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._pulp_href = None
        self._pulp_created = None
        self._plan = None
        self.discriminator = None

        if pulp_href is not None:
            self.pulp_href = pulp_href
        if pulp_created is not None:
            self.pulp_created = pulp_created
        self.plan = plan

    @property
    def pulp_href(self):
        """Gets the pulp_href of this Pulp2to3MigrationMigrationPlan.  # noqa: E501


        :return: The pulp_href of this Pulp2to3MigrationMigrationPlan.  # noqa: E501
        :rtype: str
        """
        return self._pulp_href

    @pulp_href.setter
    def pulp_href(self, pulp_href):
        """Sets the pulp_href of this Pulp2to3MigrationMigrationPlan.


        :param pulp_href: The pulp_href of this Pulp2to3MigrationMigrationPlan.  # noqa: E501
        :type: str
        """

        self._pulp_href = pulp_href

    @property
    def pulp_created(self):
        """Gets the pulp_created of this Pulp2to3MigrationMigrationPlan.  # noqa: E501

        Timestamp of creation.  # noqa: E501

        :return: The pulp_created of this Pulp2to3MigrationMigrationPlan.  # noqa: E501
        :rtype: datetime
        """
        return self._pulp_created

    @pulp_created.setter
    def pulp_created(self, pulp_created):
        """Sets the pulp_created of this Pulp2to3MigrationMigrationPlan.

        Timestamp of creation.  # noqa: E501

        :param pulp_created: The pulp_created of this Pulp2to3MigrationMigrationPlan.  # noqa: E501
        :type: datetime
        """

        self._pulp_created = pulp_created

    @property
    def plan(self):
        """Gets the plan of this Pulp2to3MigrationMigrationPlan.  # noqa: E501

        Migration Plan in JSON format  # noqa: E501

        :return: The plan of this Pulp2to3MigrationMigrationPlan.  # noqa: E501
        :rtype: object
        """
        return self._plan

    @plan.setter
    def plan(self, plan):
        """Sets the plan of this Pulp2to3MigrationMigrationPlan.

        Migration Plan in JSON format  # noqa: E501

        :param plan: The plan of this Pulp2to3MigrationMigrationPlan.  # noqa: E501
        :type: object
        """
        if self.local_vars_configuration.client_side_validation and plan is None:  # noqa: E501
            raise ValueError("Invalid value for `plan`, must not be `None`")  # noqa: E501

        self._plan = plan

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Pulp2to3MigrationMigrationPlan):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Pulp2to3MigrationMigrationPlan):
            return True

        return self.to_dict() != other.to_dict()
