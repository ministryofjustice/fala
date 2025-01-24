from django.test import SimpleTestCase, Client
from django.urls import reverse


class SearchViewFunctionTest(SimpleTestCase):
    client = Client()

    url = reverse("results")

    def test_invalid_postcode_generates_error(self):
        response = self.client.get(self.url, {"postcode": "ZZZ"})
        self.assertEqual({"postcode": ["Enter a valid postcode"]}, response.context_data["form"].errors)

    def test_template_link_and_css(self):
        response = self.client.get(reverse("adviser"))

        self.assertEqual(response.status_code, 200)

        # Ensure URL link is in response content
        self.assertContains(response, "https://www.gov.uk/check-legal-aid")

        # Ensure CSS class is in response content
        self.assertContains(response, "laa-fala__grey-box")
