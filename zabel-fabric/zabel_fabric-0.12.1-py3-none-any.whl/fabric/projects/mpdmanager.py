# Copyright (c) 2019 Martin Lafaix (martin.lafaix@external.engie.com)
#
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
#
# SPDX-License-Identifier: EPL-2.0

"""
This module provides the _ManagedProjecDefinitionManager_ class.
"""


from typing import Any, Dict, List

from zabel.commons.interfaces import Manager, ManagedProjectDefinition
from zabel.commons.utils import ensure_instance, ensure_nonemptystring

########################################################################
## Abstract ManagedProjecDefinitionManager class


class ManagedProjectDefinitionManager(Manager):
    """Abstract ManagedProjectDefinition manager.

    Provides a default implementation for the set of features a managed
    project definition manager implementation must provide:

    - constructor (`__init__`)
    - `list_managedprojects`
    - `get_managedproject`
    - `create_managedproject`
    - `update_managedproject`

    Concrete classes deriving this abstract class must implement the
    following methods if they want to use the provided defaults:

    - `get_managedproject_key`
    - `get_key_managedproject`
    - `is_managedproject_key`

    The constructor, if overwritten, must take a metadata definition as
    a parameter, which is expected to be a dictionary with at least the
    following entries:

    - `storage (dict)`: a dictionary
    - `instances (class)`: a class

    `storage` is expected to contain a `type` entry (a class inheriting
    _CollectionStorage_).  It may contain other entries, as required by
    the said storage class.

    `instances` is a class inheriting _ManagedProjectDefinition_.
    """

    def __init__(self, configuration: Dict[str, Any]) -> None:
        self.configuration = configuration
        self._storage = configuration['storage']['type'](configuration)

    # abstract methods

    def get_managedproject_key(self, project_id: str) -> str:
        """Return the storage key for project_id.

        This method converts a project_id to the corresponding storage
        key.

        # Required parameters

        - `project_id`: a non-empty string

        # Returned value

        A non-empty string.
        """
        raise NotImplementedError

    def get_key_managedproject(self, key: str) -> str:
        """Return the project_id for storage key.

        This method converts a storage key to the corresponding
        project_id.

        It is only called on keys that are managed project definition
        keys.

        # Required parameters

        - `key`: a non-empty string

        # Returned value

        A non-empty string.
        """
        raise NotImplementedError

    def is_managedproject_key(self, key: str) -> bool:
        """Return True if key is a managed project definition key.

        The underlying storage collection may contain objects that are
        not managed project definitions.  This method is used to
        differentiate those.

        # Required parameters

        - `key`: a non-empty string

        # Returned value

        A boolean
        """
        raise NotImplementedError

    # default implementation

    def list_managedprojects(self) -> List[Dict[str, Any]]:
        """Return list of managed projects on platform.

        # Returned value

        A list.  Each item in the list is a dictionary with the
        following entries:

        - `project_id`: a string
        - `last_modified`: a timestamp or None
        """
        return [
            {
                'project_id': self.get_key_managedproject(item['key']),
                'last_modified': item.get('last_modified', None),
            }
            for item in self._storage.list()
            if self.is_managedproject_key(item['key'])
        ]

    def get_managedproject(self, project_id: str) -> ManagedProjectDefinition:
        """Return managed project details.

        # Required parameters

        - `project_id`: a non-empty string

        # Returned value

        Please refer to the concrete managed project definition used for
        more information on the returned value format.
        """
        ensure_nonemptystring('project_id')

        obj = self._storage.read(self.get_managedproject_key(project_id))
        mpd: ManagedProjectDefinition = self.configuration['instances']
        return mpd.from_dict(obj)

    def create_managedproject(
        self, project_id: str, project: ManagedProjectDefinition
    ) -> None:
        """Create new managed project.

        # Required parameters

        - `project_id`: a non-empty string
        - `project`: a dictionary

        `project_id` must not be the ID of an existing managed project.
        If it is, an _ApiError_ exception will be raised.
        """
        ensure_nonemptystring('project_id')
        ensure_instance('project', dict)

        self._storage.create(self.get_managedproject_key(project_id), project)

    def update_managedproject(
        self, project_id: str, project: ManagedProjectDefinition
    ) -> None:
        """Update managed project definition.

        # Required parameters

        - `project_id`: a non-empty string
        - `project`: a dictionary

        If no existing managed project with the provided ID exists,
        an _ApiError_ exception is raised.
        """
        ensure_nonemptystring('project_id')
        ensure_instance('project', dict)

        self._storage.update(self.get_managedproject_key(project_id), project)
