# Copyright (c) 2019 Martin Lafaix (martin.lafaix@external.engie.com)
#
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
#
# SPDX-License-Identifier: EPL-2.0

"""
This module provides a basic _ManagedAccountManager_ helper managing
collections of managed accounts.
"""

from typing import Any, Dict

from zabel.commons.interfaces import ManagedAccount, Manager


########################################################################
########################################################################


class ManagedAccountManager(Manager):
    """Abstract ManagedAccount manager.

    Provides a default implementation for the set of features a managed
    account manager implementation must provide:

    - constructor (`__init__`)
    - ...

    The constructor, if overwritten, must take a metadata definition as
    a parameter, which is expected to be a dictionary with at least the
    following entries:

    - `storage (dict)`: a dictionary
    - `instances (class)`: a class

    `storage` is expected to contain a `type` entry (a class inheriting
    _CollectionStorage_).  It may contain other entries, as required by
    the said storage class.

    `instances` is a class inheriting _ManagedAccount_.
    """

    def __init__(self, configuration: Dict[str, Any]) -> None:
        self.configuration = configuration
        self._storage = configuration['storage']['type'](configuration)

    def get_managedaccount(self, canonical_id: str) -> ManagedAccount:
        raise NotImplementedError

    def create_managedaccount(
        self, canonical_id: str, account: ManagedAccount
    ) -> None:
        raise NotImplementedError

    def update_managedaccount(
        self, canonical_id: str, account: ManagedAccount
    ) -> None:
        raise NotImplementedError
