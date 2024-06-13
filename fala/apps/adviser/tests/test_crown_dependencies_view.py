from django.test import SimpleTestCase, Client, override_settings
from django.urls import reverse
import bs4


@override_settings(FEATURE_FLAG_NO_MAP=True)
class PostcodeValidationTest(SimpleTestCase):
    client = Client()
    url = reverse("search")

    def test_guernsey_postcode(self):
        data = {"postcode": "GY1"}
        response = self.client.get(self.url, data)
        self.assertContains(response, "The postcode GY1 is in Guernsey")

    def test_northern_ireland_postcode(self):
        data = {"postcode": "BT93 8AD"}
        response = self.client.get(self.url, data)
        self.assertContains(response, "The postcode BT93 8AD is in Northern Ireland")

    def test_valid_scottish_postcode(self):
        data = {"postcode": "AB11 5BN"}
        response = self.client.get(self.url, data)
        self.assertContains(response, "These results cover England and Wales.")

    def dont_test_valid_english_postcode(self):
        data = {"postcode": "M2 3WQ"}
        response = self.client.get(self.url, data)
        self.assertContains(response, "in order of closeness to")

    def test_lowercase_postcode_passes(self):
        # Lower case postcode string
        data = {"postcode": "im4"}
        response = self.client.get(self.url, data)
        self.assertContains(response, "The postcode IM4 is in the Isle of Man")

    def test_change_search_button_and_form_is_visible(self):
        data = {"postcode": "IM4"}
        response = self.client.get(self.url, data)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        form = soup.find("form", {"action": "/", "method": "get"})
        button = soup.find("button", {"type": "submit", "data-module": "govuk-button"})
        self.assertIsNotNone(form)
        self.assertIsNotNone(button)
        self.assertEqual(button.text.strip(), "Change search")


@override_settings(FEATURE_FLAG_NO_MAP=True)
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
