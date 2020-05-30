# coding: utf-8

"""
    Finnhub API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from finnhub.configuration import Configuration


class StockTranscripts(object):
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
        'id': 'str',
        'title': 'str',
        'time': 'datetime',
        'year': 'int',
        'quarter': 'int'
    }

    attribute_map = {
        'id': 'id',
        'title': 'title',
        'time': 'time',
        'year': 'year',
        'quarter': 'quarter'
    }

    def __init__(self, id=None, title=None, time=None, year=None, quarter=None, local_vars_configuration=None):  # noqa: E501
        """StockTranscripts - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._title = None
        self._time = None
        self._year = None
        self._quarter = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if title is not None:
            self.title = title
        if time is not None:
            self.time = time
        if year is not None:
            self.year = year
        if quarter is not None:
            self.quarter = quarter

    @property
    def id(self):
        """Gets the id of this StockTranscripts.  # noqa: E501

        Transcript's ID used to get the <a href=\"#transcripts\">full transcript</a>.  # noqa: E501

        :return: The id of this StockTranscripts.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this StockTranscripts.

        Transcript's ID used to get the <a href=\"#transcripts\">full transcript</a>.  # noqa: E501

        :param id: The id of this StockTranscripts.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def title(self):
        """Gets the title of this StockTranscripts.  # noqa: E501

        Title.  # noqa: E501

        :return: The title of this StockTranscripts.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this StockTranscripts.

        Title.  # noqa: E501

        :param title: The title of this StockTranscripts.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def time(self):
        """Gets the time of this StockTranscripts.  # noqa: E501

        Time of the event.  # noqa: E501

        :return: The time of this StockTranscripts.  # noqa: E501
        :rtype: datetime
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this StockTranscripts.

        Time of the event.  # noqa: E501

        :param time: The time of this StockTranscripts.  # noqa: E501
        :type: datetime
        """

        self._time = time

    @property
    def year(self):
        """Gets the year of this StockTranscripts.  # noqa: E501

        Year of earnings result in the case of earnings call transcript.  # noqa: E501

        :return: The year of this StockTranscripts.  # noqa: E501
        :rtype: int
        """
        return self._year

    @year.setter
    def year(self, year):
        """Sets the year of this StockTranscripts.

        Year of earnings result in the case of earnings call transcript.  # noqa: E501

        :param year: The year of this StockTranscripts.  # noqa: E501
        :type: int
        """

        self._year = year

    @property
    def quarter(self):
        """Gets the quarter of this StockTranscripts.  # noqa: E501

        Quarter of earnings result in the case of earnings call transcript.  # noqa: E501

        :return: The quarter of this StockTranscripts.  # noqa: E501
        :rtype: int
        """
        return self._quarter

    @quarter.setter
    def quarter(self, quarter):
        """Sets the quarter of this StockTranscripts.

        Quarter of earnings result in the case of earnings call transcript.  # noqa: E501

        :param quarter: The quarter of this StockTranscripts.  # noqa: E501
        :type: int
        """

        self._quarter = quarter

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
        if not isinstance(other, StockTranscripts):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, StockTranscripts):
            return True

        return self.to_dict() != other.to_dict()
