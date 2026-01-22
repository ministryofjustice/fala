from django.test import SimpleTestCase, Client, override_settings
from django.urls import reverse
from fala.common.test_utils.helpers import parse_html, find_element


class MaintenanceModeTest(SimpleTestCase):
    client = Client()
    url = reverse("results")

    data = {"name": "foo", "categories": ["deb", "edu"]}

    maintenance_mode_h1 = "Sorry, the service is unavailable"

    @override_settings(FEATURE_FLAG_MAINTENANCE_MODE=True)
    def test_maintenance_mode_viewable_when_flag_set(self):
        response = self.client.get(self.url, self.data)
        self.assertContains(response, self.maintenance_mode_h1)

    @override_settings(FEATURE_FLAG_MAINTENANCE_MODE=False)
    def test_maintenance_mode_hidden_when_flag_unset(self):
        response = self.client.get(self.url, self.data)
        self.assertNotContains(response, self.maintenance_mode_h1)


class AccessibilityViewTest(SimpleTestCase):
    client = Client()

    url = reverse("accessibility_statement")

    def test_shows_new_accessibility_statement(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Accessibility statement for Find a legal advisor")


class ErrorPageTest(SimpleTestCase):
    client = Client()
    url = reverse("results")

    def test_raises_404_when_page_number_does_not_exist(
        self,
    ):
        response = self.client.get(self.url, {"postcode": "SE11", "page": 4566})
        self.assertEqual(response.status_code, 404)


class LanguageSwitcherTest(SimpleTestCase):
    client = Client()
    url = reverse("results")

    data = {"name": "foo", "categories": ["deb", "edu"]}

    def test_language_switcher_visible(self):
        response = self.client.get(self.url, self.data)
        html = parse_html(response.content)
        language_switcher = find_element(html, "div", "language-switcher")
        self.assertIsNotNone(language_switcher)
