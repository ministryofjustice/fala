from django.test import SimpleTestCase, Client, override_settings
from django.urls import reverse


@override_settings(FEATURE_FLAG_NO_MAP=True)
class SearchViewFunctionTest(SimpleTestCase):
    client = Client()

    url = reverse("adviser")

    def test_postcode_search(self):
        response = self.client.get(self.url, {"postcode": "PE31"})
        self.assertEqual(200, response.status_code)

    def test_invalid_postcode_generates_error(self):
        response = self.client.get(self.url, {"postcode": "ZZZ"})
        self.assertEqual({"postcode": ["Postcode not found"]}, response.context_data["form"].errors)


@override_settings(FEATURE_FLAG_NO_MAP=True)
class NewSearchViewTemplate(SimpleTestCase):
    client = Client()

    def test_tempalte_link_and_css(self):
        response = self.client.get(reverse("adviser"))

        self.assertEqual(response.status_code, 200)

        # Ensure URL link is in response content
        self.assertContains(response, "https://www.gov.uk/check-legal-aid")

        # Ensure CSS class is in response content
        self.assertContains(response, "laa-fala__grey-box")
