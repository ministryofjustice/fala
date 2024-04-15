from django.test import SimpleTestCase, Client
from django.urls import reverse


class SearchViewFunctionTest(SimpleTestCase):
    client = Client()

    url = reverse("adviser")

    def test_postcode_search(self):
        response = self.client.get(self.url, {"postcode": "PE31"})
        self.assertEqual(response.status_code, 200)

    def test_postcode_search_zero_results(self):
        response = self.client.get(self.url, {"postcode": "ZZZ"})
        self.assertContains(response, "There are no results matching your search criteria")
