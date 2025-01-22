from django.test import SimpleTestCase, Client
from django.urls import reverse
import bs4


class PostcodeValidationTest(SimpleTestCase):
    client = Client()
    url = reverse("results")

    def test_region_postcodes(self):
        test_cases = [
            # Guernsey Postcode
            {"postcode": "GY1 2HU", "message": "The postcode GY1 2HU is in Guernsey"},
            # Northern Ireland Postcode
            {"postcode": "BT93 8AD", "message": "The postcode BT93 8AD is in Northern Ireland"},
            # Isle of Man Postcode
            {"postcode": "IM4 2HT", "message": "The postcode IM4 2HT is in the Isle of Man"},
            # Jersey Postcode
            {"postcode": "JE2 3FN", "message": "The postcode JE2 3FN is in Jersey"},
            # English Postcode
            {"postcode": "M2 3WQ", "message": "in order of closeness to"},
            # Scottish Postcode
            {"postcode": "AB11 5BN", "message": "These results cover England and Wales."},
            # Lower case Postcode still works out region.
            {"postcode": "im4", "message": "The postcode IM4 is in the Isle of Man"},
            # Invalid post code, results are found on search
            {"postcode": "AB11 9EE", "message": "Enter a valid postcode"},
            {"postcode": "IM4 TESTTTTTTTTTTTT", "message": "Enter a valid postcode"},
        ]

        for case in test_cases:
            with self.subTest(postcode=case["postcode"]):
                data = {"postcode": case["postcode"]}
                response = self.client.get(self.url, data)
                self.assertContains(response, case["message"])

    def test_border_region_postcodes(self):
        test_cases = [
            # English Postcode on Scottish border
            {"postcode": "TD15 1UY", "message": "These results cover England and Wales"},
            {"postcode": "TD15", "message": "These results cover England and Wales"},
        ]

        for case in test_cases:
            with self.subTest(postcode=case["postcode"]):
                data = {"postcode": case["postcode"]}
                response = self.client.get(self.url, data)
                self.assertNotContains(response, case["message"])

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

    def test_back_link_is_visible(self):
        data = {"tailored_results": "true", "categories": "immas", "postcode": "IM4"}
        response = self.client.get(self.url, data)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        back_link = soup.find("a", class_="govuk-back-link")
        self.assertIsNotNone(back_link, "Back button is not visible on the results page.")


class InvalidPostcodeTest(SimpleTestCase):
    client = Client()
    url = reverse("results")

    def test_invalid_postcodes_error_messages(self):
        invalid_postcodes = ["ML3 9PP", "INVALID1", "ZZ20 7QQ"]  # Add more invalid postcodes as needed
        expected_messages = ["There is a problem", "Enter a valid postcode"]

        for postcode in invalid_postcodes:
            with self.subTest(postcode=postcode):
                data = {"postcode": postcode}
                response = self.client.get(self.url, data)

                # Check that each expected message is in the response
                for message in expected_messages:
                    self.assertContains(
                        response,
                        message,
                        msg_prefix=f"Failed on postcode '{postcode}' - Expected message: '{message}' - ",
                    )
