from django.test import SimpleTestCase, Client
from django.urls import reverse


class SearchViewFunctionTest(SimpleTestCase):
    client = Client()

    url = reverse("adviser")

    def test_postcode_search(self):
        response = self.client.get(self.url, {"postcode": "PE31"})
        self.assertEqual(200, response.status_code)

    def test_invalid_postcode_generates_error(self):
        response = self.client.get(self.url, {"postcode": "ZZZ"})
        self.assertEqual({"postcode": ["Postcode not found"]}, response.context_data["form"].errors)
