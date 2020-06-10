#!/usr/bin/python
# -*- coding: utf-8 -*-

from contactcenter.core import Service

from contactcenter.contact.data import OrganizationContact
from contactcenter.contact.persistence import ContactDAO

PERSON_CONTACT = 'user'
SERVICE_CONTACT = 'service'
ORGANIZATION_CONTACT = 'organization'


class ContactService(Service):

    def __init__(self, dao: ContactDAO):
        super().__init__()
        self.dao: ContactDAO = dao

    def count_all(self):
        return self.dao.count()

    def list(self, skip=0, limit=10, sort_key='_id', sort_dir='1'):
        # TODO: Change sort setting
        return self.dao.find_all(skip, limit, [(sort_key, sort_dir)])

    def get_one_by_id(self, uid):
        return self.dao.find_one_by_key(uid)

    def create(self, first_name, last_name, phone_numbers, email_addr):
        self.create_personal_contact(first_name, last_name, phone_numbers, email_addr)

    def create_personal_contact(self, first_name, last_name, phone_numbers, email_addr, organization=None):
        """ Create a new contact
        :param first_name: The first name of the contact
        :param last_name: The last name of the contact
        :param phone_numbers: The phone numbers to reach the contact
        :param email_addr: The email address of the contact
        :param organization: The name of the organization
        :return: id of the created contact
        """
        data_set = {'name': '{} {}'.format(first_name, last_name),
                    'type': PERSON_CONTACT,
                    'first_name': first_name,
                    'last_name': last_name,
                    'organization': organization,
                    'phone_numbers': phone_numbers,
                    'email_addr': email_addr}
        inserted_id = self.dao.insert(data_set)
        return inserted_id

    def create_service_contact(self, name, phone_numbers, email_addr, organization=None):
        """ Create a new service contact
        :param name: The name of the contact
        :param phone_numbers: The phone numbers to reach the contact
        :param email_addr: The email address of the contact
        :param organization: The name of the organization
        :return: id of the created contact
        """
        data_set = {'name': name,
                    'type': SERVICE_CONTACT,
                    'organization': organization,
                    'phone_numbers': phone_numbers,
                    'email_addr': email_addr}
        inserted_id = self.dao.insert(data_set)
        return inserted_id

    def create_organization_contact(self, name, phone_numbers, email_addr):
        """ Create a new service contact
        :param name: The name of the contact
        :param phone_numbers: The phone numbers to reach the contact
        :param email_addr: The email address of the contact
        :return: id of the created contact
        """
        data_set = {'name': name,
                    'type': ORGANIZATION_CONTACT,
                    'organization': name,
                    'phone_numbers': phone_numbers,
                    'email_addr': email_addr}
        inserted_id = self.dao.insert(data_set)
        return inserted_id

    def create_organization_contact(self, contact: OrganizationContact):
        """ Create a new service contact
        :param contact: The contact details
        :return: id of the created contact
        """
        data_set = {'name': contact.name,
                    'type': contact.type,
                    'organization': contact.name,
                    'phone_numbers': contact.phone_numbers,
                    'email_addr': contact.email_addr}
        # TODO: merge with props
        inserted_id = self.dao.insert(data_set)
        return inserted_id


    def bulk_create(self, data):
        return self.dao.insert(data)

    def update(self, **kwargs):
        raise NotImplementedError()

    def delete_one_by_id(self, iud):
        return self.dao.delete(iud)

    def get_one_by_email_addr(self, email_addr):
        contact = self.dao.find_one_by_email_addr(email_addr)
        return contact

    def get_one_by_phone_number(self, phone_num):
        contact = self.dao.find_one_by_phone_number(phone_num)
        return contact

    def lookup_by_type_and_name(self, contact_type, contact_name):
        query = {
            'name': contact_name,
            'type': contact_type
        }
        contacts = self.dao.find(query)
        return contacts
