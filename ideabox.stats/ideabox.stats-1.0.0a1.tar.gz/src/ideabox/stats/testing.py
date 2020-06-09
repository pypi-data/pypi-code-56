# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import ideabox.stats


class IdeaboxStatsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        self.loadZCML(package=ideabox.stats)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "ideabox.stats:default")


IDEABOX_STATS_FIXTURE = IdeaboxStatsLayer()


IDEABOX_STATS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(IDEABOX_STATS_FIXTURE,), name="IdeaboxStatsLayer:IntegrationTesting"
)


IDEABOX_STATS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(IDEABOX_STATS_FIXTURE,), name="IdeaboxStatsLayer:FunctionalTesting"
)


IDEABOX_STATS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(IDEABOX_STATS_FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, z2.ZSERVER_FIXTURE),
    name="IdeaboxStatsLayer:AcceptanceTesting",
)
