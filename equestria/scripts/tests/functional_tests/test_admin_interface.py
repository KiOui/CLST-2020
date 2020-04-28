from equestria.tests.functional_tests.meta import GenericFuncTest


class TestAdminInterface(GenericFuncTest):
    """Tests basic UI elements."""

    fixtures = ["simple_pipelines"]

    def test_admin_interface(self):
        """Test if user is greeted by welcome text."""
        self.navigate("admin")
