"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFPlone.utils import get_installer
from test_project.testing import TEST_PROJECT_INTEGRATION_TESTING

import unittest


class TestSetup(unittest.TestCase):
    """Test that test_project is properly installed."""

    layer = TEST_PROJECT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.setup = self.portal.portal_setup
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if test_project is installed."""
        self.assertTrue(self.installer.is_product_installed("test_project"))

    def test_browserlayer(self):
        """Test that ITEST_PROJECTLayer is registered."""
        from plone.browserlayer import utils
        from test_project.interfaces import ITEST_PROJECTLayer

        self.assertIn(ITEST_PROJECTLayer, utils.registered_layers())

    def test_latest_version(self):
        """Test latest version of default profile."""
        self.assertEqual(
            self.setup.getLastVersionForProfile("test_project:default")[0],
            "20230504001",
        )


class TestUninstall(unittest.TestCase):

    layer = TEST_PROJECT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("test_project")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if test_project is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("test_project"))

    def test_browserlayer_removed(self):
        """Test that ITEST_PROJECTLayer is removed."""
        from plone.browserlayer import utils
        from test_project.interfaces import ITEST_PROJECTLayer

        self.assertNotIn(ITEST_PROJECTLayer, utils.registered_layers())
