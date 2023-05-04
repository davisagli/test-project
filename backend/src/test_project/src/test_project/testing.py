from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE

import test_project


class TEST_PROJECTLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=test_project)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "test_project:default")
        applyProfile(portal, "test_project:initial")


TEST_PROJECT_FIXTURE = TEST_PROJECTLayer()


TEST_PROJECT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(TEST_PROJECT_FIXTURE,),
    name="TEST_PROJECTLayer:IntegrationTesting",
)


TEST_PROJECT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(TEST_PROJECT_FIXTURE, WSGI_SERVER_FIXTURE),
    name="TEST_PROJECTLayer:FunctionalTesting",
)


TEST_PROJECTACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        TEST_PROJECT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="TEST_PROJECTLayer:AcceptanceTesting",
)
