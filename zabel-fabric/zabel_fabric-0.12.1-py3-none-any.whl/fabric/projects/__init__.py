# Copyright (c) 2019 Martin Lafaix (martin.lafaix@external.engie.com)
#
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
#
# SPDX-License-Identifier: EPL-2.0

"""
This module implements the specifics for the Zabel managed projects.

It provides a _DomainProviderManagedProjectDefinition_ subclass that can
be used to model many projects definitions.

It also provides a _ManagedProjectDefinitionManager_ class.
"""

__all__ = [
    'DomainProviderManagedProjectDefinition',
    'ManagedProjectDefinitionManager',
]

from .domainprovidermpd import DomainProviderManagedProjectDefinition

from .mpdmanager import ManagedProjectDefinitionManager
