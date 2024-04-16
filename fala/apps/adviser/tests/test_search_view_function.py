from django.test import SimpleTestCase, Client, override_settings
from django.urls import reverse


@override_settings(FEATURE_FLAG_NO_MAP=True)
class SearchViewFunctionTest(SimpleTestCase):
    client = Client()

    url = reverse("search")

    def test_postcode_search(self):
        response = self.client.get(self.url, {"postcode": "PE31"})
        self.assertEqual(200, response.status_code)

    def test_invalid_postcode_generates_error(self):
        response = self.client.get(self.url, {"postcode": "ZZZ"})
        self.assertContains(response, "Postcode not found")

    def test_postcode_name_category_search_has_good_result(self):
        response = self.client.get(self.url, {"postcode": "PE30", "name": "bu", "categories": "deb"})
        self.assertEqual(200, response.status_code)

    def test_postcode_name_category_search_heading_closeness(self):
        response = self.client.get(self.url, {"postcode": "PE30", "name": "bu", "categories": "deb"})
        self.assertContains(response, "in order of closeness to")

    def test_postcode_name_category_search_heading_matching(self):
        response = self.client.get(self.url, {"postcode": "PE30", "name": "bu", "categories": "deb"})
        self.assertContains(response, "matching")
