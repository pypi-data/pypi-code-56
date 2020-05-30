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


class StockCandles(object):
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
        'o': 'list[float]',
        'h': 'list[float]',
        'l': 'list[float]',
        'c': 'list[float]',
        'v': 'list[float]',
        't': 'list[int]',
        's': 'str'
    }

    attribute_map = {
        'o': 'o',
        'h': 'h',
        'l': 'l',
        'c': 'c',
        'v': 'v',
        't': 't',
        's': 's'
    }

    def __init__(self, o=None, h=None, l=None, c=None, v=None, t=None, s=None, local_vars_configuration=None):  # noqa: E501
        """StockCandles - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._o = None
        self._h = None
        self._l = None
        self._c = None
        self._v = None
        self._t = None
        self._s = None
        self.discriminator = None

        if o is not None:
            self.o = o
        if h is not None:
            self.h = h
        if l is not None:
            self.l = l
        if c is not None:
            self.c = c
        if v is not None:
            self.v = v
        if t is not None:
            self.t = t
        if s is not None:
            self.s = s

    @property
    def o(self):
        """Gets the o of this StockCandles.  # noqa: E501

        List of open prices for returned candles.  # noqa: E501

        :return: The o of this StockCandles.  # noqa: E501
        :rtype: list[float]
        """
        return self._o

    @o.setter
    def o(self, o):
        """Sets the o of this StockCandles.

        List of open prices for returned candles.  # noqa: E501

        :param o: The o of this StockCandles.  # noqa: E501
        :type: list[float]
        """

        self._o = o

    @property
    def h(self):
        """Gets the h of this StockCandles.  # noqa: E501

        List of high prices for returned candles.  # noqa: E501

        :return: The h of this StockCandles.  # noqa: E501
        :rtype: list[float]
        """
        return self._h

    @h.setter
    def h(self, h):
        """Sets the h of this StockCandles.

        List of high prices for returned candles.  # noqa: E501

        :param h: The h of this StockCandles.  # noqa: E501
        :type: list[float]
        """

        self._h = h

    @property
    def l(self):
        """Gets the l of this StockCandles.  # noqa: E501

        List of low prices for returned candles.  # noqa: E501

        :return: The l of this StockCandles.  # noqa: E501
        :rtype: list[float]
        """
        return self._l

    @l.setter
    def l(self, l):
        """Sets the l of this StockCandles.

        List of low prices for returned candles.  # noqa: E501

        :param l: The l of this StockCandles.  # noqa: E501
        :type: list[float]
        """

        self._l = l

    @property
    def c(self):
        """Gets the c of this StockCandles.  # noqa: E501

        List of close prices for returned candles.  # noqa: E501

        :return: The c of this StockCandles.  # noqa: E501
        :rtype: list[float]
        """
        return self._c

    @c.setter
    def c(self, c):
        """Sets the c of this StockCandles.

        List of close prices for returned candles.  # noqa: E501

        :param c: The c of this StockCandles.  # noqa: E501
        :type: list[float]
        """

        self._c = c

    @property
    def v(self):
        """Gets the v of this StockCandles.  # noqa: E501

        List of volume data for returned candles.  # noqa: E501

        :return: The v of this StockCandles.  # noqa: E501
        :rtype: list[float]
        """
        return self._v

    @v.setter
    def v(self, v):
        """Sets the v of this StockCandles.

        List of volume data for returned candles.  # noqa: E501

        :param v: The v of this StockCandles.  # noqa: E501
        :type: list[float]
        """

        self._v = v

    @property
    def t(self):
        """Gets the t of this StockCandles.  # noqa: E501

        List of timestamp for returned candles.  # noqa: E501

        :return: The t of this StockCandles.  # noqa: E501
        :rtype: list[int]
        """
        return self._t

    @t.setter
    def t(self, t):
        """Sets the t of this StockCandles.

        List of timestamp for returned candles.  # noqa: E501

        :param t: The t of this StockCandles.  # noqa: E501
        :type: list[int]
        """

        self._t = t

    @property
    def s(self):
        """Gets the s of this StockCandles.  # noqa: E501

        Status of the response. This field can either be ok or no_data.  # noqa: E501

        :return: The s of this StockCandles.  # noqa: E501
        :rtype: str
        """
        return self._s

    @s.setter
    def s(self, s):
        """Sets the s of this StockCandles.

        Status of the response. This field can either be ok or no_data.  # noqa: E501

        :param s: The s of this StockCandles.  # noqa: E501
        :type: str
        """

        self._s = s

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
        if not isinstance(other, StockCandles):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, StockCandles):
            return True

        return self.to_dict() != other.to_dict()
