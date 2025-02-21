from django.test import SimpleTestCase, Client
from django.urls import reverse
from fala.common.test_utils.helpers import parse_html, find_element


class ResultsViewTest(SimpleTestCase):
    client = Client()
    url = reverse("results")

    def test_back_button_is_visible_on_results_page(self):
        self.data = {"tailored_results": "true", "postcode": "SW11", "categories": ["wb"]}
        response = self.client.get(self.url, self.data)
        self.assertEqual(response.status_code, 200)
        html = parse_html(response.content)
        back_link = find_element(html, "a", "govuk-back-link")
        self.assertIsNotNone(back_link, "Back button is not visible on the results page.")

    def test_single_category_results_for_mental_health(self):
        self.data = {"tailored_results": "true", "postcode": "SE11", "categories": ["mhe"]}
        response = self.client.get(self.url, self.data)
        self.assertContains(response, "Your closest legal aid advisers for mental health")

    def test_single_category_results_for_family(self):
        self.data = {"tailored_results": "true", "postcode": "SE11", "categories": ["mat"]}
        response = self.client.get(self.url, self.data)
        self.assertContains(response, "Your closest legal aid advisers and family mediators")

    def test_single_category_results_for_hlpas(self):
        self.data = {"tailored_results": "true", "postcode": "SE11", "categories": ["hlpas"]}
        response = self.client.get(self.url, self.data)
        self.assertContains(response, "Your closest legal aid advisers for the Housing Loss Prevention Advice Service")

    def test_pagination_links_with_hlpas(self):
        self.data = {"tailored_results": "true", "postcode": "SE11", "categories": ["hlpas"]}
        response = self.client.get(self.url, self.data)
        self.assertContains(response, "Your closest legal aid advisers for the Housing Loss Prevention Advice Service")
        html = parse_html(response.content)
        next_link = find_element(html, "a", "govuk-link govuk-pagination__link")
        next_href = next_link.get("href")
        self.assertIn("tailored_results=true", next_href, "Pagination link does not contain 'tailored_results'.")
        self.assertNotIn("spam", next_href, "Pagination link surprisingly contains 'spam'.")
        next_response = self.client.get(next_href)
        self.assertEqual(next_response.status_code, 200, "Next page did not load successfully.")
