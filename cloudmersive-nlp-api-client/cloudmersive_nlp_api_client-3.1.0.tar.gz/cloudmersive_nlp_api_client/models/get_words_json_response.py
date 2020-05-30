# coding: utf-8

"""
    nlpapi

    The powerful Natural Language Processing APIs let you perform part of speech tagging, entity identification, sentence parsing, and much more to help you understand the meaning of unstructured text.  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from cloudmersive_nlp_api_client.models.word_position import WordPosition  # noqa: F401,E501


class GetWordsJsonResponse(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'words': 'list[WordPosition]'
    }

    attribute_map = {
        'words': 'Words'
    }

    def __init__(self, words=None):  # noqa: E501
        """GetWordsJsonResponse - a model defined in Swagger"""  # noqa: E501

        self._words = None
        self.discriminator = None

        if words is not None:
            self.words = words

    @property
    def words(self):
        """Gets the words of this GetWordsJsonResponse.  # noqa: E501

        Array of words  # noqa: E501

        :return: The words of this GetWordsJsonResponse.  # noqa: E501
        :rtype: list[WordPosition]
        """
        return self._words

    @words.setter
    def words(self, words):
        """Sets the words of this GetWordsJsonResponse.

        Array of words  # noqa: E501

        :param words: The words of this GetWordsJsonResponse.  # noqa: E501
        :type: list[WordPosition]
        """

        self._words = words

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(GetWordsJsonResponse, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, GetWordsJsonResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
