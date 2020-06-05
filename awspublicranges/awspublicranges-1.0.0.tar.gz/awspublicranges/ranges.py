#MIT License
#
#Copyright (c) 2020 Matthew G. Monteleone
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

# __init__.py

# Version of the realpython-reader package
__version__ = "1.0.0"

import requests
import ipaddress
from pprint import pprint
from datetime import datetime
from typing import Optional, Union
from enum import Enum

SOURCE_URL = 'https://ip-ranges.amazonaws.com/ip-ranges.json'


class AwsServices(Enum):
    AMAZON = "All Amazon"
    AMAZON_CONNECT = "AMAZON CONNECT"
    API_GATEWAY = 'API GATEWAY'
    CLOUD9 = 'CLOUD9'
    CLOUDFRONT = 'CLOUDFRONT'
    CODEBUILD = 'CODEBUILT'
    DYNAMODB = 'DYNAMODB'
    EC2 = 'EC2'
    EC2_INSTANCE_CONNECT = 'EC2 INSTANCECONNECT'
    GLOBALACCELERATOR = 'GLOBALACCELERATOR'
    ROUTE53 = 'ROUTE53'
    ROUTE53_HEALTHCHECKS = 'ROUTE53 HEALTHCHECK'
    S3 = 'S3'
    WORKSPACES_GATEWAYS = 'WORKSPACES_GATEWAYS'
    ROUTE53_HEALTHCHECKS_PUBLISHING = 'ROUTE53 HEALTHCHECKS PUBLISHING'


class AddressType(enumerate):
    v4 = 'IP V4'
    v6 = 'IP V6'


class AwsPrefix(object):
    def __init__(self, entry_dict: dict):
        self.ip_prefix: Optional[Union[ipaddress.IPv4Network, ipaddress.IPv6Network]] = None
        self.type: Optional[AddressType] = None
        try:
            self.ip_prefix = ipaddress.IPv4Network(entry_dict.get('ip_prefix'))
            self.type: AddressType = AddressType.v4
        except ipaddress.AddressValueError:
            self.ip_prefix = ipaddress.IPv6Network(entry_dict.get('ipv6_prefix'))
            self.type: AddressType = AddressType.v6
        self.region = entry_dict.get('region')
        self.service = AwsServices[entry_dict.get('service')]
        self.network_border_group = entry_dict.get('network_border_group')


class AwsIpRanges(object):
    def __init__(self):
        """Current AWS IP ranges, both v4 and v6.

        Pulls from the published json file. Includes some basic filtering functionality.

        """
        self.prefixes = list()
        self.ipv6_prefixes = list()
        try:
            raw_data = requests.get(SOURCE_URL).json()
        except Exception as e:
            raise
        self.create_date = datetime.strptime(raw_data.get('createDate'), '%Y-%m-%d-%H-%M-%S')
        self.sync_token = raw_data.get('syncToken')
        for entry in raw_data.get('prefixes'):
            self.prefixes.append(AwsPrefix(entry_dict=entry))
        for entry in raw_data.get('ipv6_prefixes'):
            self.ipv6_prefixes.append(AwsPrefix(entry_dict=entry))

    @property
    def prefixes_e2c(self):
        for each in [self.prefixes]:
            if each.service == AwsServices.EC2:
                yield each

    @property
    def prefixes_all(self):
        """All ip v4 prefixes

        """
        for each in [self.prefixes]:
            if each.service == AwsServices.AMAZON:
                yield each

    def prefixes_for_lambda(self, region_filter: str = None):
        """Prefixes filtered by service for use with lambda.

        Filters out services that can be excluded if you are grabbing ip ranges for use with aws lambda.

        :param region_filter:
        """
        amazon_ips = [item for item in self.prefixes if item.service == AwsServices.AMAZON]
        not_used_ips = [item.ip_prefix for item in self.prefixes if
                        item.service in [AwsServices.CLOUD9, AwsServices.S3, AwsServices.CLOUDFRONT,
                                         AwsServices.CODEBUILD, AwsServices.DYNAMODB, AwsServices.GLOBALACCELERATOR,
                                         AwsServices.ROUTE53]]
        for each in amazon_ips:
            if each.ip_prefix not in not_used_ips:
                if region_filter:
                    if each.ip_prefix not in not_used_ips and each.region == region_filter:
                        yield each
                else:
                    yield each

    @property
    def prefixes_for_lambda_count(self,region_filter: str = None):
        count = 0
        for each_entry in self.prefixes_for_lambda(region_filter=region_filter):
            count += 1
        return count
