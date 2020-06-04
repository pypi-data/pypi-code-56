# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.easyformplugin.poll.testing import COLLECTIVE_EASYFORMPLUGIN_POLL_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that collective.easyformplugin.poll is properly installed."""

    layer = COLLECTIVE_EASYFORMPLUGIN_POLL_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.easyformplugin.poll is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.easyformplugin.poll'))

    def test_browserlayer(self):
        """Test that ICollectiveEasyformpluginPollLayer is registered."""
        from collective.easyformplugin.poll.interfaces import (
            ICollectiveEasyformpluginPollLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectiveEasyformpluginPollLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_EASYFORMPLUGIN_POLL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['collective.easyformplugin.poll'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.easyformplugin.poll is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.easyformplugin.poll'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveEasyformpluginPollLayer is removed."""
        from collective.easyformplugin.poll.interfaces import \
            ICollectiveEasyformpluginPollLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ICollectiveEasyformpluginPollLayer,
            utils.registered_layers())
