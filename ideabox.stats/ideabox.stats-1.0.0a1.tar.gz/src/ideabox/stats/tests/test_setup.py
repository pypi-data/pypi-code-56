# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from ideabox.stats.testing import IDEABOX_STATS_INTEGRATION_TESTING

import unittest


class TestSetup(unittest.TestCase):
    """Test that ideabox.stats is properly installed."""

    layer = IDEABOX_STATS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if ideabox.stats is installed."""
        self.assertTrue(self.installer.isProductInstalled("ideabox.stats"))

    def test_browserlayer(self):
        """Test that IIdeaboxStatsLayer is registered."""
        from ideabox.stats.interfaces import IIdeaboxStatsLayer
        from plone.browserlayer import utils

        self.assertIn(IIdeaboxStatsLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = IDEABOX_STATS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = api.portal.get_tool("portal_quickinstaller")
        self.installer.uninstallProducts(["ideabox.stats"])

    def test_product_uninstalled(self):
        """Test if ideabox.stats is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled("ideabox.stats"))

    def test_browserlayer_removed(self):
        """Test that IIdeaboxStatsLayer is removed."""
        from ideabox.stats.interfaces import IIdeaboxStatsLayer
        from plone.browserlayer import utils

        self.assertNotIn(IIdeaboxStatsLayer, utils.registered_layers())
