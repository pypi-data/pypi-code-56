# coding: utf-8

"""
    nlpapi

    The powerful Natural Language Processing APIs let you perform part of speech tagging, entity identification, sentence parsing, and much more to help you understand the meaning of unstructured text.  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from cloudmersive_nlp_api_client.api_client import ApiClient


class ExtractEntitiesStringApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def extract_entities_string_post(self, value, **kwargs):  # noqa: E501
        """Extract entities from string  # noqa: E501

        Extract the named entitites from an input string.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.extract_entities_string_post(value, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str value: Input string (required)
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.extract_entities_string_post_with_http_info(value, **kwargs)  # noqa: E501
        else:
            (data) = self.extract_entities_string_post_with_http_info(value, **kwargs)  # noqa: E501
            return data

    def extract_entities_string_post_with_http_info(self, value, **kwargs):  # noqa: E501
        """Extract entities from string  # noqa: E501

        Extract the named entitites from an input string.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.extract_entities_string_post_with_http_info(value, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str value: Input string (required)
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['value']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method extract_entities_string_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'value' is set
        if ('value' not in params or
                params['value'] is None):
            raise ValueError("Missing the required parameter `value` when calling `extract_entities_string_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'value' in params:
            body_params = params['value']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/json', 'application/xml', 'text/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'text/json', 'application/xml', 'text/xml', 'application/x-www-form-urlencoded'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Apikey']  # noqa: E501

        return self.api_client.call_api(
            '/nlp/ExtractEntitiesString', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='str',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
