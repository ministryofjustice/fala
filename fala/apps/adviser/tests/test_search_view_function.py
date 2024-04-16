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

    def test_url_link_is_in_DOM(self):
        response = self.client.get(reverse("adviser"))
        self.assertEqual(response.status_code, 200)

        # Ensure URL link is in DOM
        self.assertContains(
            response,
            '<a class="govuk-link" href="https://www.gov.uk/check-legal-aid" target="_blank" rel="noopener">Check if you qualify for legal aid (opens in a new tab)</a>',
        )

        # Ensure CSS class is visible in DOM
        self.assertContains(response, '<div class="laa-fala__grey-box">')
