# Copyright (c) 2019 Martin Lafaix (martin.lafaix@external.engie.com)
#
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
#
# SPDX-License-Identifier: EPL-2.0

"""
The high-level **zabel** library.

It provides an abstraction for _platforms_, which are collections of
_services_.

## Services (Abstract Base Classes)

### Realm Abstract Class

**work in progress, not ready yet**

| Abstract&nbsp;Class | Description                                    |
| ------------------- | ---------------------------------------------- |
| _Realm_             | A collection of platforms and domains.  A realm
                        handles users and managed projects, and
                        implements the #::Service interface.           |

### Platform Abstract Class

| Abstract&nbsp;Class | Description                                    |
| ------------------- | ---------------------------------------------- |
| #::Platform         | A service that manages a collection of
                        managedservices and utilities services, with an
                        associated set of properties and datasources.
                        A platform handles users and managed projects,
                        and implements the #::Service interface.       |

## Properties Helper Classes

### Managed accounts

| Helper&nbsp;Class        | Description                               |
| ------------------------ | ----------------------------------------- |
| #::ManagedAccount        | An abstract class that represents a
                             minimal managed account.                  |
| #::ManagedAccountManager | An abstract class that handles collections
                             of managed accounts.                      |

### Managed projects

| Helper&nbsp;Class                        | Description               |
| ---------------------------------------- | ------------------------- |
| #::DomainProviderManagedProjectDefinition| An abstract class that
                                             extends the
                                             _ManagedProjectDefinition_
                                             class to cover common
                                             managed project definition
                                             needs.                    |
| #::ManagedProjectDefinitionManager       | An abstract class that
                                             handles collections of
                                             managed project
                                             definitions.              |

## Datasources Helper Classes

| Helper&nbsp;Class   | Description                                    |
| ------------------- | ---------------------------------------------- |
| #::Storage          | An interface for storage classes.              |
| #::ObjectStorage    | An interface for storage classes handling one
                        object.                                        |
| #::CollectionStorage| An interface for storage classes handling a
                        collection of objects.                         |
| #::AWSS3Storage     | An abstract class providing AWS S3 helpers.    |
| #::AWSS3Object      | A _Storage_ class for JSON files stored on a
                        S3 bucket.                                     |
| #::AWSS3Bucket      | A _Storage_ class for handling S3 buckets.     |
| #::ManagedDict      | A simple class making use of an _ObjectStorage_
                        delegate, providing a 'persistent' dictionary. |
"""

__all__ = [
    'ManagedAccount',
    'ManagedAccountManager',
    'DomainProviderManagedProjectDefinition',
    'ManagedProjectDefinitionManager',
    'Service',
    'Utility',
    'ManagedService',
    'Platform',
]


from zabel.commons.interfaces import (
    Service,
    Utility,
    ManagedService,
)

from .services import Platform
from .accounts import (
    ManagedAccount,
    ManagedAccountManager,
)
from .projects import (
    DomainProviderManagedProjectDefinition,
    ManagedProjectDefinitionManager,
)
