from django.test import TestCase
import bs4


class SingleCategorySearchResultsPageTests(TestCase):
    def setUp(self):
        self.url = "/search?categories=wb&tailored_results=true&postcode=SW11"

    def test_back_button_is_visible_on_results_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        back_link = soup.find("a", class_="govuk-back-link")
        self.assertIsNotNone(back_link, "Back button is not visible on the results page.")
