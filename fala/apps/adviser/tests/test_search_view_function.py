import bs4
from django.test import SimpleTestCase, Client, override_settings
from django.urls import reverse


@override_settings(FEATURE_FLAG_NO_MAP=True)
class SearchViewFunctionTest(SimpleTestCase):
    client = Client()

    url = reverse("search")

    def test_invalid_postcode_generates_error(self):
        response = self.client.get(self.url, {"postcode": "ZZZ"})
        self.assertEqual({"postcode": ["Enter a valid postcode"]}, response.context_data["form"].errors)


@override_settings(FEATURE_FLAG_NO_MAP=True)
class ResultsPageWithBothOrgAndPostcodeTest(SimpleTestCase):
    client = Client()
    url = reverse("search")

    data = {"postcode": "pe30", "name": "bu", "categories": "deb"}

    def test_category_search_has_just_user_input(self):
        response = self.client.get(self.url, self.data)
        self.assertContains(response, "PE30")

    def test_category_search_heading_closeness_and_matching_postcode_and_organisation(self):
        response = self.client.get(self.url, self.data)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        results_header = soup.find("span", class_="results-header")
        self.assertIsNotNone(results_header)

        # Check the content of the span
        # Regex to check an integer is present
        expected_content_pattern = r"\d+ results"
        self.assertRegex(results_header.text.strip(), expected_content_pattern)

        # Check the presence of the string
        expected_text = "in order of closeness to"
        self.assertIn(expected_text, results_header.text.strip())

        # Check the presence of specific elements
        self.assertIsNotNone(results_header.find("strong", class_="notranslate", text="PE30"))
        self.assertIsNotNone(results_header.find("strong", text="bu"))

    def test_search_parameters_box_is_visible(self):
        response = self.client.get(self.url, self.data)
        soup = bs4.BeautifulSoup(response.content, features="html.parser")
        search_params_box = soup.find("div", class_="laa-fala__grey-box")
        self.assertIsNotNone(search_params_box)

    def test_search_returns_results_list(self):
        response = self.client.get(self.url, self.data)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        results = soup.find_all("li", class_="results-list-item")
        self.assertEqual(10, len(results))

    def test_category_search_has_next_button(self):
        response = self.client.get(self.url, self.data)
        self.assertContains(response, '<div class="govuk-pagination__next">')

    def test_category_search_has_no_previous_button(self):
        response = self.client.get(self.url, self.data)
        self.assertNotContains(response, '<div class="govuk-pagination__previous">')


@override_settings(FEATURE_FLAG_NO_MAP=True)
class ResultsPageWithJustPostcodeTest(SimpleTestCase):
    client = Client()
    url = reverse("search")

    data = {"postcode": "PE30", "categories": "deb"}

    def test_category_search_heading_postcode_only(self):
        response = self.client.get(self.url, self.data)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        results_header = soup.find("span", class_="results-header")
        self.assertIsNotNone(results_header)

        # Check the content of the span
        # Regex to check an integer is present
        expected_content_pattern = r"\d+ results"
        self.assertRegex(results_header.text.strip(), expected_content_pattern)

        # Check the presence of the string
        expected_text = "in order of closeness to"
        self.assertIn(expected_text, results_header.text.strip())

        # Extract the text from the results header span
        header_text = results_header.get_text()

        # Assert that either the full stop or the string is visible
        self.assertIn(".", header_text, "Full stop after PE30 not found")

        # Check the presence of specific elements
        self.assertIsNotNone(results_header.find("strong", class_="notranslate", text="PE30"))

    def test_search_parameters_box_contains_only_postcode_and_categories(self):
        response = self.client.get(self.url, self.data)
        soup = bs4.BeautifulSoup(response.content, features="html.parser")
        search_params_box = soup.find("div", class_="laa-fala__grey-box")
        # replace the spaces in the HTML for ease of comparison
        content = search_params_box.text.replace("\n", "")
        self.assertEqual(content, "Postcode: PE30Categories: Debt Change search")


@override_settings(FEATURE_FLAG_NO_MAP=True)
class ResearchBannerTest(SimpleTestCase):
    client = Client()
    url = reverse("search")

    data = {"name": "foo", "categories": ["deb", "edu"]}

    research_message = "Help improve this legal adviser search"

    @override_settings(FEATURE_FLAG_SURVEY_MONKEY=True)
    def test_research_banner_present_when_flag_set(self):
        response = self.client.get(self.url, self.data)
        self.assertContains(response, self.research_message)

    @override_settings(FEATURE_FLAG_SURVEY_MONKEY=False)
    def test_research_banner_absent_when_flag_unset(self):
        response = self.client.get(self.url, self.data)
        self.assertNotContains(response, self.research_message)


@override_settings(FEATURE_FLAG_NO_MAP=True)
class ResultsPageWithJustOrgTest(SimpleTestCase):
    client = Client()
    url = reverse("search")

    data = {"name": "foo", "categories": ["deb", "edu"]}

    def test_search_parameters_box_contains_only_organisation_and_categories(self):
        response = self.client.get(self.url, self.data)
        soup = bs4.BeautifulSoup(response.content, features="html.parser")
        search_params_box = soup.find("div", class_="laa-fala__grey-box")
        # replace the spaces in the HTML for ease of comparison
        content = search_params_box.text.replace("\n", "")
        self.assertEqual(content, "Organisation: fooCategories: Debt, Education Change search")


@override_settings(FEATURE_FLAG_NO_MAP=True)
class NewSearchViewTemplate(SimpleTestCase):
    client = Client()

    def test_template_link_and_css(self):
        response = self.client.get(reverse("adviser"))

        self.assertEqual(response.status_code, 200)

        # Ensure URL link is in response content
        self.assertContains(response, "https://www.gov.uk/check-legal-aid")

        # Ensure CSS class is in response content
        self.assertContains(response, "laa-fala__grey-box")


@override_settings(FEATURE_FLAG_NO_MAP=True)
class NoResultsTest(SimpleTestCase):
    client = Client()

    url = reverse("search")

    response = client.get(url, {"name": "burns", "categories": "com"})

    def test_no_results(self):
        self.assertContains(self.response, "There are no results")


class AccessibilityViewTest(SimpleTestCase):
    client = Client()

    url = reverse("accessibility_statement")

    @override_settings(FEATURE_FLAG_NO_MAP=True)
    def test_shows_new_accessibility_statement(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Accessibility statement for Find a legal advisor")

    @override_settings(FEATURE_FLAG_NO_MAP=False)
    def test_shows_old_accessibility_statement(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Accessibility statement")
        self.assertNotContains(response, "Accessibility statement for Find a legal advisor")
