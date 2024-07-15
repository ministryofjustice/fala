from django.test import SimpleTestCase, Client
from django.urls import reverse
import bs4


class PostcodeValidationTest(SimpleTestCase):
    client = Client()
    url = reverse("search")

    def test_region_postcodes(self):
        test_cases = [
            {"postcode": "GY1", "message": "The postcode GY1 is in Guernsey"},
            {"postcode": "BT93 8AD", "message": "The postcode BT93 8AD is in Northern Ireland"},
            {"postcode": "IM4", "message": "The postcode IM4 is in the Isle of Man"},
            {"postcode": "JE2 3FN", "message": "The postcode JE2 3FN is in Jersey"},
            # English Postcode
            {"postcode": "M2 3WQ", "message": "in order of closeness to"},
            # Scottish Postcode
            {"postcode": "AB11 5BN", "message": "These results cover England and Wales."},
            # Lower case Postcode
            {"postcode": "im4", "message": "The postcode IM4 is in the Isle of Man"},
            # Invalid post code with no prefix numbers, results are found and search
            # Region is recognised as Scotland.
            {"postcode": "AB", "message": "These results cover England and Wales."},
        ]

        for case in test_cases:
            with self.subTest(postcode=case["postcode"]):
                data = {"postcode": case["postcode"]}
                response = self.client.get(self.url, data)
                self.assertContains(response, case["message"])

    def test_other_region_form_and_change_search_button_visible(self):
        data = {"postcode": "IM4"}
        response = self.client.get(self.url, data)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        form = soup.find("form", {"action": "/", "method": "get"})
        button = soup.find("button", {"type": "submit", "data-module": "govuk-button"})
        self.assertIsNotNone(form)
        self.assertIsNotNone(button)

        change_search_button = soup.find("button", {"id": "otherRegionChangeSearchButton"})
        self.assertIsNotNone(change_search_button)
        self.assertEqual(change_search_button.text.strip(), "Change search")


class InvalidEnglishPostcodeTest(SimpleTestCase):
    client = Client()
    url = reverse("search")
    data = {"postcode": "ZZ1 1QQ"}

    def test_there_is_a_problem(self):
        response = self.client.get(self.url, self.data)
        self.assertContains(response, "There is a problem")

    def test_error_message(self):
        response = self.client.get(self.url, self.data)
        self.assertContains(response, "Enter a valid postcode")
