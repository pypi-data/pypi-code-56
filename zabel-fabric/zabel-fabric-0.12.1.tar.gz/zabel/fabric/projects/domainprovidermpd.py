# Copyright (c) 2019 Martin Lafaix (martin.lafaix@external.engie.com)
#
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
#
# SPDX-License-Identifier: EPL-2.0

"""
This module provides a _DomainProviderManagedProjectDefinition_ class
that can be used to represent managed projects definitions.
"""

from typing import Any, Callable, Dict, List, NoReturn, Optional, Set

from zabel.commons.exceptions import ApiError
from zabel.commons.interfaces import ManagedProjectDefinition
from zabel.commons.utils import (
    ensure_in,
    ensure_nonemptystring,
    ensure_noneorinstance,
)


########################################################################
########################################################################

## managed project definitions


class DomainProviderManagedProjectDefinition(ManagedProjectDefinition):
    """Managed Project Definition with Domains and Providers.

    It extends _ManagedProjectDefinition_.

    A _DomainProviderManagedProject_ contains a set of _domains_ (e.g.
    tools or services) that themselves contain a set of _providers_
    (e.g. teams).

    Each provider contains _members_, split in _categories_, and a set
    of additional fields.

    By default there are three member categories ('admins', 'readers'
    and 'users') and one additional field ('options').

    This wrapper offers a set of helpers managing members and additional
    fields in domain providers.

    ## Usage

    If an implementation wants to make use of the offered helpers, it
    will have to declare the list of its domains in the `DOMAINS`
    attribute.

    Each domain will be able to contain any number of providers.  Those
    providers then can have members ('admins', 'users' and 'readers' by
    default, as specified by the `MEMBER_CATEGORIES` attribute) and
    additional fields ('options' by default, as specified by the
    `OTHER_CATEGORIES` attribute).

    ## Attributes

    | Attribute           | Description                                |
    | ------------------- | ------------------------------------------ |
    | `DOMAINS`           | A dictionary.  The keys are the internal
                            names (the entry in the MPD) and the values
                            are the public names (what will be used in
                            the accessors method names).<br/>
                            The internal names will be keys in the
                            managed project definition dictionaries and
                            public names will be used in accessors
                            method names.<br/>
                            Internal and public names should not start
                            with an underscore.                        |
    | `MEMBER_CATEGORIES` | A dictionary.  The keys are the members
                            categories names, and the values are their
                            types (_dict_ being the only supported
                            value).<br/>
                            The 'member' category name is reserved.    |
    | `OTHER_CATEGORIES`  | A dictionary.  The keys are the 'other'
                            categories names, and the values are their
                            types (_list_ being the only supported
                            value).                                    |

    ## Accessors

    Accessors methods for domains are automatically generated if not
    redefined in the children class.

    For each domain, the accessors methods are (assuming the default
    categories for providers):

    - `list_{public_name}s()`
    - `create_{public_name}(provider)`

    - `list_{public_name}s_members()`
    - `delete_{public_name}s_member()`

    - `list_{public_name}_admins(provider)`
    - `add_{public_name}_admin(provider, name, service='*')`
    - `remove_{public_name}_admin(provider, name, service=None)`
    - `list_{public_name}_users(provider)`
    - `add_{public_name}_user(provider, name, service='*')`
    - `remove_{public_name}_user(provider, name, service=None)`
    - `list_{public_name}_readers(provider)`
    - `add_{public_name}_reader(provider, name, service='*')`
    - `remove_{public_name}_reader(provider, name, service=None)`
    - `list_{public_name}_options(provider)`
    - `add_{public_name}_option(provider, item)`
    - `remove_{public_name}_option(provider, item)`

    In addition to those domain accessors, the following methods are
    defined:

    - `list_members()`
    - `remove_member(item)`
    - `list_domain_provider_{category}s(domain, provider)`
    - `add_domain_provider_{category}(domain, provider, item, service='*')`
    - `remove_domain_provider_{category}(domain, provider, item, service=None)`
    """

    DOMAINS: Dict[str, str] = {}
    MEMBER_CATEGORIES: Dict[str, type] = {
        'admin': list,
        'user': list,
        'reader': list,
    }
    OTHER_CATEGORIES: Dict[str, type] = {'option': list}

    def __init__(self) -> None:
        """Create a new managed project."""
        super().__init__()

        if 'member' in self.MEMBER_CATEGORIES:
            raise ApiError('Key \'member\' is reserved in MEMBER_CATEGORIES')

        for category in self.MEMBER_CATEGORIES:
            self._expose_domain_provider_membercategoryaccessor(category)
        for category in self.OTHER_CATEGORIES:
            self._expose_domain_provider_othercategoryaccessor(category)
        self['spec'] = {}
        for domain in self.DOMAINS:
            self['spec'][domain] = {}
            self._expose_accessors(domain)

    # Domains
    #

    def is_domain_publicname(self, domain: str) -> bool:
        """Return whether a domain is a domain public name."""
        return domain in self.DOMAINS.values()

    def get_domain_publicname(self, internal: str) -> str:
        """Return domain's public name."""
        return self.DOMAINS[internal]

    def get_domain_internalname(self, domain: str) -> str:
        """Return domain's internal name."""
        return [d for d in self.DOMAINS if self.DOMAINS[d] == domain][0]

    # Members
    #

    def list_members(self) -> Set[str]:
        """Return the set of domain provider members."""
        members: Set[str] = set()
        for domain in self.DOMAINS:
            members = members.union(self.list_domain_members(domain))
        return members

    def remove_member(self, member: str) -> None:
        """Remove member from all domain providers."""
        for domain in self.DOMAINS:
            self.remove_domain_member(domain, member)

    # Domains Members Helpers
    #
    # list_domain_members
    # remove_domain_member

    def list_domain_members(self, domain: str) -> Set[str]:
        """Return a set of declared domain members.

        `domain` is the domain internalname.

        # Required parameters

        - domain: a non-empty string

        # Returned value

        A set.  Each item in the set is a string.
        """
        members: Set[str] = set()
        for provider in self['spec'][domain]:
            for category in self.MEMBER_CATEGORIES:
                members = members.union(
                    m['account'] for m in provider[f'{category}s']
                )
        return members

    def remove_domain_member(self, domain: str, member: str) -> None:
        """Remove a member from all domain providers.

        `domain` is the domain internal name.

        # Required parameters

        - domain: a non-empty string
        - member: a non-empty string

        # Returned value

        None.
        """
        for provider in self['spec'][domain]:
            for category in self.MEMBER_CATEGORIES:
                members = provider[f'{category}s']
                for item in [m for m in members if m['account'] == member]:
                    members.remove(item)

    # Domains Providers Helpers
    #
    # list_domain_providers
    # create_domain_provider
    # delete_domain_provider

    def list_domain_providers(self, domain: str) -> Set[str]:
        """Return a set of declared domain providers.

        # Required parameters

        - `domain`: a non-empty string

        # Returned value

        A set.  Each item in the set is a string.
        """
        if not domain.startswith('__'):
            ensure_in('domain', self.DOMAINS)

        return set(provider['name'] for provider in self['spec'][domain])

    def create_domain_provider(
        self, domain: str, provider: str, **fields: Any
    ) -> None:
        """Add a provider to a domain.

        # Required parameters

        - `domain`: a non-empty string
        - `provider`: a non-empty string

        # Optional parameters

        - `fields`: a dictionary or None

        # Raised exceptions

        If `provider` is already declared in `domain`, an _ApiError_
        exception is raised.
        """
        ensure_nonemptystring('provider')
        ensure_noneorinstance('fields', dict)
        if not domain.startswith('__'):
            ensure_in('domain', self.DOMAINS)

        if provider in self.list_domain_providers(domain):
            raise ApiError(
                'Provider %s already declared in domain %s.'
                % (provider, domain)
            )

        _definition = {'name': provider}
        self['spec'][domain].append(_definition)

        for category in self.MEMBER_CATEGORIES:
            _definition[f'{category}s'] = self.MEMBER_CATEGORIES[category]()
        for category in self.OTHER_CATEGORIES:
            _definition[f'{category}s'] = self.OTHER_CATEGORIES[category]()
        if fields:
            for field in fields:
                _definition[field] = fields[field]

    def delete_domain_provider(self, domain: str, provider: str) -> None:
        """Remove provider.

        # Required parameters

        - `domain`: a non-empty string
        - `provider`: a non-empty string

        # Raised exceptions

        If `provider` is not declared in `domain`, an _ApiError_
        exception is raised.
        """
        ensure_nonemptystring('provider')
        if not domain.startswith('__'):
            ensure_in('domain', self.DOMAINS)

        if provider not in self.list_domain_providers(domain):
            raise ApiError(
                'Provider %s not declared in domain %s.' % (provider, domain)
            )

        for item in [p for p in self['spec'][domain] if p['name'] == provider]:
            self['spec'][domain].remove(item)

    def list_domain_provider_category_members(
        self, domain: str, provider: str, category: str
    ) -> List[Dict[str, Any]]:
        """Return specified members for domain provider.

        `domain` is the domain internal name.

        # Required parameters

        - `domain`: a non-empty string
        - `provider`: a non-empty string
        - `category`: a non-empty string

        # Returned value

        A list of dictionaries.

        # Raised exceptions

        Raises an _ApiError_ exception if `provider`, `domain`, or
        `category` are not known.
        """
        ensure_nonemptystring('domain')
        ensure_nonemptystring('provider')
        ensure_nonemptystring('category')

        try:
            for p in self['spec'][domain]:
                if p['name'] == provider:
                    return list(p[category])
            else:
                self._raise_keyerror(domain, provider, category)
        except KeyError:
            self._raise_keyerror(domain, provider, category)

    # private helpers

    def _raise_keyerror(
        self, domain: str, provider: str, item: str, key: Optional[str] = None
    ) -> NoReturn:
        if domain not in self['spec']:
            raise ApiError('Domain %s not known.' % domain)
        if provider not in self['spec'][domain]:
            raise ApiError(
                'Provider %s not known in domain %s.' % (provider, domain)
            )
        if item not in self['spec'][domain][provider]:
            raise ApiError(
                'Item %s not known in provider %s for domain %s.'
                % (item, provider, domain)
            )
        raise ApiError(
            '%s %s not known in provider %s for domain %s.'
            % (item.title(), key, provider, domain)
        )

    def _add_category_member_option(
        self,
        domain: str,
        provider: str,
        category: str,
        member: str,
        option: str,
    ) -> None:
        """Add option to member, or create member with specified option."""
        ensure_nonemptystring('domain')
        ensure_nonemptystring('provider')
        ensure_nonemptystring('category')

        try:
            for p in self['spec'][domain]:
                if p['name'] == provider:
                    members = p[category]
                    break
            else:
                self._raise_keyerror(domain, provider, category)
            for m in members:
                if m['account'] == member:
                    if option in m['options']:
                        raise ApiError(
                            '%s %s already set to %s for provider %s.'
                            % (category, member, option, provider)
                        )
                    m['options'].append(option)
                    break
            else:
                members.append({'account': member, 'options': [option]})
        except KeyError:
            self._raise_keyerror(domain, provider, category)

    def _remove_category_member_option(
        self,
        domain: str,
        provider: str,
        category: str,
        member: str,
        option: Optional[str],
    ) -> None:
        ensure_nonemptystring('domain')
        ensure_nonemptystring('provider')
        ensure_nonemptystring('category')

        try:
            for p in self['spec'][domain]:
                if p['name'] == provider:
                    members = p[category]
                    break
            else:
                self._raise_keyerror(domain, provider, category, member)
            for m in members:
                if m['account'] == member:
                    if option is not None:
                        if option in m['options']:
                            m['options'].remove(option)
                        else:
                            raise ApiError(
                                '%s %s not set to %s for provider %s.'
                                % (category, member, option, provider)
                            )
                        if option is None or not m['options']:
                            members.remove(m)
                        break
            else:
                self._raise_keyerror(domain, provider, category, member)
        except KeyError:
            self._raise_keyerror(domain, provider, category, member)

    def _list_domain_provider_category_items(
        self, domain: str, provider: str, category: str
    ) -> List[str]:
        ensure_nonemptystring('domain')
        ensure_nonemptystring('provider')
        ensure_nonemptystring('category')

        try:
            for p in self['spec'][domain]:
                if p['name'] == provider:
                    return list(p[category])
            else:
                self._raise_keyerror(domain, provider, category)
        except KeyError:
            self._raise_keyerror(domain, provider, category)

    def _add_category_item(
        self, domain: str, provider: str, category: str, item: str
    ) -> None:
        ensure_nonemptystring('domain')
        ensure_nonemptystring('provider')
        ensure_nonemptystring('category')

        try:
            for p in self['spec'][domain]:
                if p['name'] == provider:
                    if item in p[category]:
                        raise ApiError(
                            '%s %s already declared for provider %s'
                            % (category, item, provider)
                        )
                    p[category].append(item)
                    break
            else:
                self._raise_keyerror(domain, provider, category)
        except KeyError:
            self._raise_keyerror(domain, provider, category)

    def _remove_category_item(
        self, domain: str, provider: str, category: str, item: str
    ) -> None:
        ensure_nonemptystring('domain')
        ensure_nonemptystring('provider')
        ensure_nonemptystring('category')

        try:
            for p in self['spec'][domain]:
                if p['name'] == provider:
                    if item not in p['category']:
                        raise ApiError(
                            '%s %s not declared for provider %s'
                            % (category, item, provider)
                        )
                    p[category].remove(item)
                    break
            else:
                self._raise_keyerror(domain, provider, category)
        except KeyError:
            self._raise_keyerror(domain, provider, category)

    # accessors generators

    def _create_method(self, name: str, body: Callable[..., Any]) -> None:
        if not hasattr(self, name):
            self.__setattr__(name, body)

    def _expose_member_category_accessors(
        self, domain: str, name: str, category: str
    ) -> None:
        """Create undefined accessors for domain member categories.

        Will attempt to create the following methods:

        - `list_{domain}_{category}s(provider)`
        - `add_{domain>_{category}(provider, member, service='*')`
        - `remove_{domain}_{category}(provider, member, service=None)`

        If a method already exists, it is left as-is.
        """
        cat = '%ss' % category
        self._create_method(
            'list_%s_%ss' % (name, category),
            lambda provider: self.list_domain_provider_category_members(
                domain, provider, cat
            ),
        )
        self._create_method(
            'add_%s_%s' % (name, category),
            lambda provider, member, service='*': self._add_category_member_option(
                domain, provider, cat, member, service
            ),
        )
        self._create_method(
            'remove_%s_%s' % (name, category),
            lambda provider, member, service=None: self._remove_category_member_option(
                domain, provider, cat, member, service
            ),
        )

    def _expose_other_category_accessors(
        self, domain: str, name: str, category: str
    ) -> None:
        """Create undefined accessors for domain 'other' categories.

        Will attempt to create the following methods:

        - `list_{domain}_{category}s(provider)`
        - `add_{domain}_{category}(provider, item)`
        - `remove_{domain}_{category}(provider, item)`

        If a method already exists, it is left as-is.
        """
        cat = '%ss' % category
        self._create_method(
            'list_%s_%ss' % (name, category),
            lambda provider: self._list_domain_provider_category_items(
                domain, provider, cat
            ),
        )
        self._create_method(
            'add_%s_%s' % (name, category),
            lambda provider, option: self._add_category_item(
                domain, provider, cat, option
            ),
        )
        self._create_method(
            'remove_%s_%s' % (name, category),
            lambda provider, option: self._remove_category_item(
                domain, provider, cat, option
            ),
        )

    def _expose_accessors(self, domain: str) -> None:
        """Create accessors for domain, if not already defined.

        Will attempt to create the following methods:

        - `list_{domain}s()`
        - `create_{domain}(provider)`
        - `delete_{domain}(provider)`
        - `list_{domain}s_members()`
        - `remove_{domain}s_member()`

        Will also attempt to create the category accessors.

        If a method already exists, it is left as-is.
        """
        name = self.DOMAINS[domain]

        # providers
        self._create_method(
            'list_%ss' % name, lambda: self.list_domain_providers(domain)
        )
        self._create_method(
            'create_%s' % name,
            lambda provider: self.create_domain_provider(domain, provider),
        )
        self._create_method(
            'delete_%s' % name,
            lambda provider: self.delete_domain_provider(domain, provider),
        )

        self._create_method(
            'list_%ss_members' % name, lambda: self.list_domain_members(domain)
        )

        self._create_method(
            'remove_%ss_member' % name,
            lambda member: self.remove_domain_member(domain, member),
        )

        # providers members
        for category in self.MEMBER_CATEGORIES:
            self._expose_member_category_accessors(domain, name, category)

        for category in self.OTHER_CATEGORIES:
            self._expose_other_category_accessors(domain, name, category)

    def _expose_domain_provider_membercategoryaccessor(
        self, category: str
    ) -> None:
        """Create domain_provider accessors for member category.

        Will attempt to create the following methods:

        - `list_domain_provider_{category}s(domain, provider)`
        - `add_domain_provider_{category}(domain, provider, member,
            service='*')`
        - `remove_domain_provider_{category}(domain, provider, member,
            service=None)`

        If a method already exists, it is left as-is.
        """
        cat = '%ss' % category
        self._create_method(
            'list_domain_provider_%ss' % category,
            lambda domain, provider: self.list_domain_provider_category_members(
                domain, provider, cat
            ),
        )
        self._create_method(
            'add_domain_provider_%s' % category,
            lambda domain, provider, member, service='*': self._add_category_member_option(
                domain, provider, cat, member, service
            ),
        )
        self._create_method(
            'remove_domain_provider_%s' % category,
            lambda domain, provider, member, service=None: self._remove_category_member_option(
                domain, provider, cat, member, service
            ),
        )

    def _expose_domain_provider_othercategoryaccessor(
        self, category: str
    ) -> None:
        """Create domain_provider accessors for other category.

        Will attempt to create the following methods:

        - `list_domain_provider_{category}s(domain, provider)`
        - `add_domain_provider_{category}(domain, provider, item)`
        - `remove_domain_provider_{category}(domain, provider, item)`

        If a method already exists, it is left as-is.
        """
        cat = '%ss' % category
        self._create_method(
            'list_domain_provider_%ss' % category,
            lambda domain, provider: self._list_domain_provider_category_items(
                domain, provider, cat
            ),
        )
        self._create_method(
            'add_domain_provider_%s' % category,
            lambda domain, provider, member: self._add_category_item(
                domain, provider, cat, member
            ),
        )
        self._create_method(
            'remove_domain_provider_%s' % category,
            lambda domain, provider, member: self._remove_category_item(
                domain, provider, cat, member
            ),
        )
