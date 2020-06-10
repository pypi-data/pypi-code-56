#!/usr/bin/python
# -*- coding: utf-8 -*-

PERSON_CONTACT = 'person'
SERVICE_CONTACT = 'service'
ORGANIZATION_CONTACT = 'organization'


class Contact:
    ID = '_id'
    NAME = 'name'
    EMAIL_ADDR = 'email_addr'
    PHONE_NUMBERS = 'phone_numbers'

    def __init__(self, name, type, phone_numbers, email_addr, **kwargs):
        self.name = name
        self.type = type
        self.phone_numbers = phone_numbers
        self.email_addr = email_addr
        self.props = kwargs


class OrganizationContact(Contact):

    def __init__(self, name, phone_numbers, email_addr, **kwargs):
        super().__init__(name, ORGANIZATION_CONTACT, phone_numbers, email_addr, **kwargs)


class ServiceContact(Contact):

    def __init__(self, name, phone_numbers, email_addr, **kwargs):
        super().__init__(name, SERVICE_CONTACT, phone_numbers, email_addr, **kwargs)


class PersonContact(Contact):

    def __init__(self, first_name, last_name, phone_numbers, email_addr, **kwargs):
        super().__init__('{} {}'.format(first_name, last_name), ORGANIZATION_CONTACT, phone_numbers, email_addr,
                         **kwargs)
        self.first_name = first_name
        self.last_name = last_name


class OrgUnit:
    NAMESPACE = 'namespace'
    CODE = 'code'
    REF = 'ref'
    ID = '_id'
    NAME = 'name'
    PARENT = 'parent'
    ENABLED = 'enabled'
    BUSINESS_LINE = 'business_line'

    def __init__(self, namespace: str, code: str, name: str, **kwargs):
        self.namespace = namespace
        self.code = code
        self.name = name
        self.props = kwargs
