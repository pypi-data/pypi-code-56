""" EEA Aliases
"""
import logging
from zope.interface import Interface
from plone.app.upgrade.utils import alias_module
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("eea.aliases")

try:
    from App.interfaces import IPersistentExtra
except ImportError:
    class IPersistentExtra(Interface):
        '''IPersistentExtra interface'''
        pass
    alias_module('App.interfaces.IPersistentExtra', IPersistentExtra)
    LOGGER.warn(
        "Alias registered for missing: App.interfaces.IPersistentExtra")


try:
    from App.interfaces import IUndoSupport
except ImportError:
    class IUndoSupport(Interface):
        '''IUndoSupport interface'''
        pass
    alias_module('App.interfaces.IUndoSupport', IUndoSupport)
    LOGGER.warn("Alias registered for missing: App.interfaces.IUndoSupport")


try:
    from OFS.interfaces import IFTPAccess as IOFSFTPAccess
except ImportError:
    class IOFSFTPAccess(Interface):
        '''interface used for alias'''
        pass
    alias_module('OFS.interfaces.IFTPAccess', IOFSFTPAccess)
    LOGGER.warn("Alias registered for missing: OFS.interfaces.IFTPAccess")


try:
    from webdav.interfaces import IFTPAccess
except ImportError:
    class IFTPAccess(Interface):
        '''interface used for alias'''
        pass
    alias_module('webdav.interfaces.IFTPAccess', IFTPAccess)
    LOGGER.warn("Alias registered for missing: webdav.interfaces.IFTPAccess")

try:
    from webdav.interfaces import IDAVCollection  # noqa
except ImportError:
    class IDAVCollection(Interface):
        '''interface used for alias'''
        pass
    alias_module("webdav.interfaces.IDAVCollection", IDAVCollection)
    LOGGER.warn(
        "Alias registered for missing: webdav.interfaces.IDAVCollection")

try:
    from webdav.interfaces import IDAVResource  # noqa
except ImportError:
    class IDAVResource(Interface):
        '''interface used for alias'''
        pass
    alias_module("webdav.interfaces.IDAVResource", IDAVResource)
    LOGGER.warn("Alias registered for missing: webdav.interfaces.IDAVResource")


try:
    from webdav.interfaces import IWriteLock  # noqa
except ImportError:
    class IWriteLock(Interface):
        '''interface used for alias'''
        pass
    alias_module("webdav.interfaces.IWriteLock", IWriteLock)
    LOGGER.warn("Alias registered for missing: webdav.interfaces.IWriteLock")

try:
    from webdav.EtagSupport import EtagBaseInterface  # noqa
except ImportError:
    class EtagBaseInterface(Interface):
        '''interface used for alias'''
        pass
    alias_module('webdav.EtagSupport.EtagBaseInterface', EtagBaseInterface)
    LOGGER.warn(
        "Alias registered for missing: webdav.EtagSupport.EtagBaseInterface")


try:
    from Products.ResourceRegistries.interfaces.settings import \
        IResourceRegistriesSettings
except ImportError:
    class IResourceRegistriesSettings(Interface):
        '''interface used for alias'''
        pass
    alias_module('Products.ResourceRegistries.interfaces.settings.'
                 'IResourceRegistriesSettings',
                 IResourceRegistriesSettings)
    LOGGER.warn("Alias registered for missing: Products.ResourceRegistries."
                "interfaces.settings.IResourceRegistriesSettings")


try:
    from Products.RedirectionTool.RedirectionTool import RedirectionTool
except ImportError:
    from Persistence import Persistent

    class RedirectionTool(Persistent):
        '''blanc used for alias'''
        pass
    alias_module(
        'Products.RedirectionTool.RedirectionTool.RedirectionTool',
        RedirectionTool)
    LOGGER.warn(
        "Alias registered for missing: "
        "Products.RedirectionTool.RedirectionTool.RedirectionTool")


try:
    # pylint: disable=ungrouped-imports
    from plone.dexterity.schema import SchemaModuleFactory
    from zope.component.hooks import getSiteManager

    SM = getSiteManager()
    SM.registerUtility(factory=SchemaModuleFactory,
                       name="plone.dexterity.schema.generated")
except Exception as err:
    LOGGER.exception(err)
else:
    LOGGER.warn("Manually register plone.dexterity.schema.generated utility")

#
# Custom renames for zodbupdate
#
RENAME_DICT = {

    # 'mypackage.mymodule ClassName':'otherpackage.othermodule OtherClass'

}
