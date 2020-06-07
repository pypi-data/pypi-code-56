# Copyright (c) 2019 Martin Lafaix (martin.lafaix@external.engie.com)
#
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
#
# SPDX-License-Identifier: EPL-2.0

"""
The **zabel.fabric**  _Platform_ abstract class.
"""

from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Mapping,
    MutableMapping,
    Optional,
)

from zabel.commons.exceptions import ApiError
from zabel.commons.interfaces import (
    Service,
    ManagedService,
    ManagedProjectDefinition,
    ManagedAccount,
)
from zabel.commons.utils import (
    api_call,
    ensure_instance,
    ensure_nonemptystring,
    ensure_noneorinstance,
)

from ..accounts import ManagedAccountManager
from ..projects import ManagedProjectDefinitionManager


########################################################################
## Service


class Platform(Service):
    """A _Platform_ service.

    A platform is a collection of _services_ with associated _members_,
    _properties_, and _managed projects_.

    This class has no public constructor.  You have to use the
    #::amac.make_platform() factory method to instantiate a _Platform_
    object.

    # Services

    Services are of two kinds: _utilities_, that are not hosting managed
    projects, and _managed services_, that are hosting managed projects.

    Utilities are for example directories or external services (AWS,
     Azure, ...).

    Managed services are typically tools (Artifactory, Jira, ...).

    If no credentials are provided for a service, the service will not
    be instantiated (except if it is defined as being an _anonymous_
    service).

    # Members

    A platform has associated members (members of the managed services
    that are associated to the platform).

    Members have _canonical_ IDs, which are platform-specific.

    Each service must implement the necessary translation methods, to
    and from those canonical IDs from and to their internal IDs.

    Canonical IDs are strings.  Internal IDs are service-specific
    (but typically either strings or integers).

    # Properties

    Properties are data objects attached to a platform.  Those
    properties can be literals (say, a text description) or 'live'
    objects (instances of a class, for example #::Manager or
    #::ManagedDict).

    Properties have a name and a value.  They are singletons.

    Each platform has at least two associated properties,
    `managedprojectdefinitions`, which is an object implementing the
    #::ManagedProjectDefinitionManager interface and `managedaccounts`,
    which is an object implementing the #::ManagedAccountManager
    interface.

    # Managed projects

    Managed projects each have a definition.  Those definitions are
    objects implementing the #::ManagedProjectDefinition interface.

    Managed projects can be 'pushed' to the platform managed services.

    # Managed accounts

    Managed accounts represent the managed projects members, and may
    possibly represent former managed projects members, as well as
    other members (for example, platform administrators, ...).

    Managed accounts can be queried or disabled.

    ## Platform attributes

    In addition to the methods it provides, 3 attributes are exposed:

    | Attribute     | Description                                      |
    | ------------- | ------------------------------------------------ |
    | `definition`  | A dictionary, the platform definition            |
    | `credentials` | A #::Credentials object                          |
    | `services`    | A dictionary where keys are service names and
                      values are instances of the specified services   |
    """

    def __init__(
        self, _: str, definition: Dict[str, Any], credentials: Credentials
    ) -> None:
        self.definition = definition
        self.credentials = credentials
        self.services: Dict[str, Service] = {}
        self._mpdmanager: Optional[ManagedProjectDefinitionManager] = None
        self._mamanager: Optional[ManagedAccountManager] = None

        for name, service in definition['services'].items():
            if service.get('anonymous', False) or credentials.contains(name):
                self.services[name] = _make_service(name, service, credentials)
        for service in self.services.values():
            service.platform = self

    def __str__(self) -> str:
        return f'{self.__class__.__name__}: {self.definition["name"]!r}'

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self.definition["name"]!r}>'

    ####################################################################
    # platform members
    #
    # list_members
    # get_member

    @api_call
    def list_members(self) -> Dict[str, Dict[str, Any]]:
        """Return the members of the service.

        Member of the platform are those of the managed services it
        contains.

        # Returned value

        A dictionary.  The keys are the canonical IDs and the values are
        dictionaries.

        Those dictionaries have one entry per platform service in which
        the member is known.

        Entries are the name of the service, and values are the service
        member representation.
        """

        def _add_member(
            members: Dict[str, Dict[str, Any]],
            name: str,
            member: str,
            user: Any,
        ) -> None:
            if member not in members:
                members[member] = dict()
            members[member][name] = user

        members: Dict[str, Dict[str, Any]] = dict()
        for name, service in self.services.items():
            if not isinstance(service, ManagedService):
                continue
            service_members = service.list_members()
            for member in service_members:
                _add_member(members, name, member, service_members[member])

        return members

    @api_call
    def get_member(self, member_id: str) -> Dict[str, Any]:
        """Return the user details.

        # Required parameters

        - member_id: a string

        `member_id` is the canonical member ID.

        # Returned value

        A dictionary.  See #list_members() for more information on
        its content.

        # Raised exceptions

        An _ApiError_ exception is raised if `member_id` is not a member
        of the platform.
        """
        ensure_nonemptystring('member_id')

        member = dict()
        for name, service in self.services.items():
            if isinstance(service, ManagedService):
                try:
                    member[name] = service.get_member(member_id)
                except ApiError:
                    pass

        if not member:
            raise ApiError('Member %s not found on platform' % member_id)

        return member

    ####################################################################
    # platform renderer
    #

    def render(self, target: Any = None) -> None:
        """Render the platform object for the specified target."""
        raise NotImplementedError

    ####################################################################
    # platform properties
    #

    _properties: Dict[str, Any] = {}

    def get_property(self, name: str) -> Any:
        """Return platform property.

        # Required parameters

        - name: a string

        # Returned value

        A data object, which is either the literal value as stored
        in the platform definition or an instance of a class specified
        in the `type` entry of the literal.

        This class is expected to have a constructor with one parameter,
        which will be the dictionary associated with the property.

        For example, if the 'properties' section in the platform
        definition contains the following:

        ```python
        {
            'foo': [1, 2, 3],
            'bar': {
                'type': Something,
                'arg': [1, 2, 3]
            }
        }
        ```

        `get_property('foo')` will return `[1, 2, 3]`.

        `get_property('bar')` will return the result of the following
        call:

        ```python
        Something({'type': Something, 'arg': [1, 2, 3]})
        ```

        Properties are singletons.
        """
        if name not in self._properties:
            what = self.definition['properties'][name]
            if isinstance(what, dict) and 'type' in what:
                self._properties[name] = what['type'](what)
            else:
                self._properties[name] = what
        return self._properties[name]

    ####################################################################
    # platform managed accounts
    #
    # get_managedaccount
    # create_managedaccount
    # update_managedaccount

    @api_call
    def get_managedaccount(self, canonical_id: str) -> ManagedAccount:
        """Return managed account details.

        Please refer to the concrete managed account used for more
        information on its content.

        # Required parameters

        - canonical_id: a non-empty string

        # Return value

        An instance of _ManagedAccount_.
        """
        ensure_nonemptystring('canonical_id')

        return self._get_mamanager().get_managedaccount(canonical_id)

    @api_call
    def create_managedaccount(
        self, canonical_id: str, account: ManagedAccount
    ) -> None:
        """Create new managed account.

        # Required parameters

        - canonical_id: a string
        - account: a #::ManagedAccount object

        # Raised exceptions

        `canonical_id` must not be the ID of an existing managed
        account.  If it is, an _ApiError_ exception will be raised.
        """
        ensure_nonemptystring('canonical_id')
        ensure_instance('account', ManagedAccount)

        self._get_mamanager().create_managedaccount(canonical_id, account)

    @api_call
    def update_managedaccount(
        self, canonical_id: str, account: ManagedAccount
    ) -> None:
        """Update managed account

        # Required parameters

        - canonical_id: a string
        - account: a #::ManagedAccount object

        # Raised exceptions

        If no existing managed account with the provided ID exists,
        an _ApiError_ exception is raised.
        """
        ensure_nonemptystring('canonical_id')
        ensure_instance('account', ManagedAccount)

        self._get_mamanager().update_managedaccount(canonical_id, account)

    ####################################################################
    # platform managed projects
    #
    # list_managedprojects
    # get_managedproject
    # create_managedproject
    # update_managedproject
    # push_managedproject
    # render_managedproject

    # reading/writing projects

    @api_call
    def list_managedprojects(self) -> List[Dict[str, Any]]:
        """Return list of managed projects on platform.

        # Returned value

        Each item in the list is a dictionary with the following
        entries:

        - project_id: a string
        - last_modified: a _datetime.datetime_ object
        """
        return self._get_mpdmanager().list_managedprojects()

    @api_call
    def get_managedproject(self, project_id: str) -> ManagedProjectDefinition:
        """Return managed project details.

        Please refer to the concrete managed project definition used for
        more information on its content.

        # Required parameters

        - project_id: a non-empty string

        # Returned value

        An instance of #::ManagedProjectDefinition.
        """
        ensure_nonemptystring('project_id')

        return self._get_mpdmanager().get_managedproject(project_id)

    @api_call
    def create_managedproject(
        self, project_id: str, project: ManagedProjectDefinition
    ) -> None:
        """Create new managed project.

        # Required parameters

        - project_id: a string
        - project: a dictionary

        # Raised exceptions

        `project_id` must not be the ID of an existing managed project.
        If it is, an _ApiError_ exception will be raised.
        """
        ensure_nonemptystring('project_id')
        ensure_instance('project', dict)

        self._get_mpdmanager().create_managedproject(project_id, project)

    @api_call
    def update_managedproject(
        self, project_id: str, project: ManagedProjectDefinition
    ) -> None:
        """Update managed project definition.

        # Required parameters

        - project_id: a string
        - project: a dictionary

        # Raised exceptions

        If no existing managed project with the provided ID exists,
        an _ApiError_ exception is raised.
        """
        ensure_nonemptystring('project_id')
        ensure_instance('project', dict)

        self._get_mpdmanager().update_managedproject(project_id, project)

    def render_managedproject(
        self, project_id: str, target: Any = None
    ) -> Any:
        """Render the managed project on the specified target."""
        raise NotImplementedError

    # pushing projects

    def get_push_strategy(
        self, project: ManagedProjectDefinition, context: Mapping[str, Any]
    ) -> Iterable[Callable[[ManagedProjectDefinition], None]]:
        """Return the push strategy.

        !!! important
            Subclasses must implement this method if the platform allows
            for managed project pushes.

        This method is called by #push_managedproject() to get the _push
        strategy_ for the given project and context.

        A push strategy is an iterable that returns _push steps_.

        A push step is a function that takes one argument, the project
        definition, and returns no value but may raise an exception.

        Steps are called in order by #push_managedproject().

        If a step raises an exception, the possible remaining steps are
        ignored, and the rollback strategy will be queried and executed
        if the exception is an _ApiError_ exception.

        If all steps complete successfully, #push_managedproject() will
        return True.

        # Required parameters

        - project: a _ManagedProjectDefinition_
        - context: a dictionary

        # Returned value

        A possibly empty list of push steps (callables taking a
        #::ManagedProjectDefinition as their only parameter).
        """
        raise NotImplementedError

    def get_rollback_strategy(
        self,
        project: ManagedProjectDefinition,
        trace: Iterable[Callable[[ManagedProjectDefinition], None]],
        ex: ApiError,
    ) -> Iterable[Callable[[ManagedProjectDefinition], None]]:
        """Return the failed push rollback strategy.

        This function is called by #push_managedproject() if an
        _ApiError_ exception occurs while executing the push strategy.

        By default, it returns a _rollback strategy_ that simply
        re-raise the exception.

        A platform may choose to refine this rollback strategy,
        possibly allowing for 'clean' failures.

        A rollback strategy is an iterable that returns _rollback
        steps_.

        A rollback step is a function that takes one argument, the
        project definition (a #::ManagedProjectDefinition).

        If the returned strategy is empty, nothing will be attempted,
        and the #push_managedproject() function will simply return
        False.

        If the returned strategy is not empty, steps will be called in
        order.  If a step raises an exception, it will be propagated
        (and the possible remaining steps will be ignored).

        If all steps complete successfully (i.e., they don't raise an
        exception), the #push_managedproject() function will return
        False with no further ado.

        # Required parameters

        - project: a #::ManagedProjectDefinition
        - trace: a list of performed actions, the last one having
          raised an _ApiError_ exception
        - ex: the raised exception

        If `trace` is the empty list, the exception was raised while
        acquiring the push strategy.

        # Returned value

        A possibly empty list of rollback steps (callables taking a
        single parameter, a #::ManagedProjectDefinition).
        """
        # pylint: disable=unused-argument,no-self-use
        def _raise(_: ManagedProjectDefinition) -> None:
            raise ex

        return [_raise]

    @api_call
    def push_managedproject(
        self,
        project_id: str,
        context: Optional[MutableMapping[str, Any]] = None,
    ) -> bool:
        """Push (aka publish) managed project on platform.

        This method queries the platform push strategy by calling
        #get_push_strategy() and execute it.

        If an _ApiError_ exception occurs while executing the push
        strategy, a roll-back strategy is queried by calling
        #get_rollback_strategy() and is then performed.

        # Required parameters

        - project_id: a non-empty string

        # Optional parameters

        - context: a dictionary (None by default)

        If `context` is provided, a transient `_trace` entry will be
        added (or, if already there, will be reinitialized) and will
        contain the resulting execution _trace_ (the collection of
        values passed to info, warning, and debug).  The `_trace` value
        is a list of tuples: (stamp, severity, message).  The list is
        ordered (most recent entry last).

        # Returned value

        A boolean.  True if the managed project is successfully pushed,
        False if a successful rollback was performed.

        Raises an exception otherwise.
        """
        ensure_nonemptystring('project_id')
        ensure_noneorinstance('context', dict)

        project = self.get_managedproject(project_id)
        if context is None:
            context = {}

        trace = []
        try:
            for step in self.get_push_strategy(project, context):
                trace.append(step)
                step(project)
        except ApiError as ex:
            context['_trace'] = project['_transient']['trace']
            for step in self.get_rollback_strategy(project, trace, ex):
                step(project)
            return False

        context['_trace'] = project['_transient']['trace']
        return True

    # Helpers

    def _get_mpdmanager(self) -> ManagedProjectDefinitionManager:
        if self._mpdmanager is None:
            self._mpdmanager = self.get_property('managedprojectdefinitions')
            if self._mpdmanager is None:
                raise ApiError('ManagedProjectDefinitionManager is None.')
            self._mpdmanager.platform = self
        return self._mpdmanager

    def _get_mamanager(self) -> ManagedAccountManager:
        if self._mamanager is None:
            self._mamanager = self.get_property('managedaccounts')
            if self._mpdmanager is None:
                raise ApiError('ManagedAccountManager is None.')
            self._mamanager.platform = self
        return self._mamanager
