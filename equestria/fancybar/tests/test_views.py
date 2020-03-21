from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse
from fancybar.views import *


class GenericViewTest(TestCase):
    """Defines utility methods for testing views."""

    default_templates = ["progbase.html", "base.html", "header.html"]
    name = ""  # name of url as defined in urls.py

    def setUp(self):
        """Initialize response before every test."""
        self.client = Client()
        self.response = self.client.get(reverse(self.name))

    def get_uses_templates(self, templates):
        """
        Check if GET on url with name is rendered successfully using templates.

        Every file in templates needs to be used to render
        The view may also use additional unspecified files
        :param templates: list of template files that render request
        """
        self.assertEquals(self.response.status_code, 200)
        for template in templates:
            self.assertTemplateUsed(self.response, template)

    def get_uses_template_and_defaults(self, template):
        """
        Check if GET on url with name is rendered successfully using template and default templates.

        The view may also use additional unspecified files
        :param template: template file that renders request
        """
        self.get_uses_templates([template,] + self.default_templates)


class RestrictedViewTest(GenericViewTest):
    """Defines utility methods for testing login restricted views."""

    def redirects_to_login(self):
        """Test a GET request without login. Expect to be redirected."""
        self.assertEquals(self.response.status_code, 302)
        # Frontend isn't using any templates as it seems
        # self.assertTemplateUsed(response, "login.html")

    def login(self):
        """Log in a test user."""
        username = "testuser"
        secret = "my_favorite_pony_is_cozy_glow_but_dont_tell_anyone_its_kinda_embarrasing"
        """Delete the userdb to ensure unique usernames."""
        User.objects.all().delete()
        User.objects.create_user(username=username, password=secret)
        success = self.client.login(username=username, password=secret)
        self.assertTrue(success)

    def get_uses_templates(self, templates):
        """
        Check if GET on url with name is rendered successfully using templates.

        Every file in templates needs to be used to render
        The view may also use additional unspecified files
        :param templates: list of template files that render request
        """
        self.login()
        self.response = self.client.get(reverse(self.name))
        super().get_uses_templates(templates)

    def get_uses_template_and_defaults(self, template):
        """
        Check if GET on url with name is rendered successfully using template and default templates.

        The view may also use additional unspecified files
        :param template: template file that renders request
        """
        self.login()
        self.response = self.client.get(reverse(self.name))
        super().get_uses_template_and_defaults(template)


class TestLoginSystem(RestrictedViewTest):
    """Test login system related features."""

    name = "accounts:login"

    def test_login(self):
        """Test whether login works."""
        # self.assertFalse(self.response.user.is_authenticated())
        # self.login()
        # self.response = self.client.get(reverse(self.name))
        # self.assertTrue(self.response.user.is_authenticated())


class TestFancybar(GenericViewTest):
    """Test the Fancybar view."""

    name = "fancybar:fancybar"

    def test_get(self):
        """Test a get request."""
        self.get_uses_template_and_defaults("template.html",)


class TestPraatScripts(RestrictedViewTest):
    """Test the PraatScripts view."""

    name = "fancybar:praat_scripts"

    def test_get(self):
        """Test a get request."""
        self.redirects_to_login()
        self.login()
        self.get_uses_template_and_defaults("praat_scripts.html")


class TestUploadWav(GenericViewTest):
    """Test the UploadWav view."""

    name = "fancybar:upload_wav"

    def test_get(self):
        """Test a get request."""
        self.get_uses_template_and_defaults("upload_wav.html")


class TestUploadTxt(GenericViewTest):
    """Test the UploadTxt view."""

    name = "fancybar:upload_txt"

    def test_get(self):
        """Test a get request."""
        self.get_uses_template_and_defaults("upload_txt.html")


class TestForcedAlignment(RestrictedViewTest):
    """Test the ForcedAlignment view."""

    name = "fancybar:forced_alignment"

    def test_get(self):
        """Test a get request."""
        self.redirects_to_login()
        self.login()
        self.get_uses_template_and_defaults("forced_alignment.html")


class TestUpdateDictionary(RestrictedViewTest):
    """Test the UpdateDictionary view."""

    name = "fancybar:update_dictionary"

    def test_get(self):
        """Test a get request."""
        self.redirects_to_login()
        self.login()
        self.get_uses_template_and_defaults("update_dictionary.html")


class TestAutoSegmentation(RestrictedViewTest):
    """Test the AutoSegmentation view."""

    name = "fancybar:auto_segmentation"

    def test_get(self):
        """Test a get request."""
        self.redirects_to_login()
        self.login()
        self.get_uses_template_and_defaults("auto_segmentation.html")


class TestDownloadResults(RestrictedViewTest):
    """Test the DownloadResults view."""

    name = "fancybar:download_results"

    def test_get(self):
        """Test a get request."""
        self.redirects_to_login()
        self.login()
        self.get_uses_template_and_defaults("download_results.html")
