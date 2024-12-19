import bs4
from django.test import SimpleTestCase, Client, override_settings
from django.urls import reverse


class SearchViewFunctionTest(SimpleTestCase):
    client = Client()

    url = reverse("search")

    def test_invalid_postcode_generates_error(self):
        response = self.client.get(self.url, {"postcode": "ZZZ"})
        self.assertEqual({"postcode": ["Enter a valid postcode"]}, response.context_data["form"].errors)


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

    def test_back_link_is_not_visible(self):
        response = self.client.get(self.url, self.data)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        back_link = soup.find("a", class_="govuk-back-link")
        self.assertIsNone(back_link)


class PaginationTest(SimpleTestCase):
    client = Client()
    url = reverse("search")

    def test_prev_pagination_link_contains_category(self):
        data = {"postcode": "PE30", "categories": "deb", "page": "2"}

        response = self.client.get(self.url, data)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        next = soup.find("div", class_="govuk-pagination__prev")
        link = next.find("a").get("href")
        self.assertEqual("/search?page=1&postcode=PE30&name=&categories=deb", link)

    def test_prev_pagination_link_with_multiple_categories(self):
        data = {"postcode": "PE30", "categories": ["deb", "aap"], "page": "2"}

        response = self.client.get(self.url, data)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        next = soup.find("div", class_="govuk-pagination__prev")
        link = next.find("a").get("href")
        self.assertEqual("/search?page=1&postcode=PE30&name=&categories=deb&categories=aap", link)

    def test_pagination_link_without_category(self):
        data = {"postcode": "PE30", "page": "2"}

        response = self.client.get(self.url, data)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        next = soup.find("div", class_="govuk-pagination__prev")
        link = next.find("a").get("href")
        self.assertEqual("/search?page=1&postcode=PE30&name=", link)

    def test_next_pagination_link_contains_category(self):
        data = {"postcode": "PE30", "categories": "deb", "page": "2"}

        response = self.client.get(self.url, data)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        next = soup.find("div", class_="govuk-pagination__next")
        link = next.find("a").get("href")
        self.assertEqual("/search?page=3&postcode=PE30&name=&categories=deb", link)

    def test_2nd_pagination_link_contains_category(self):
        data = {"postcode": "PE30", "categories": "deb", "page": "2"}

        response = self.client.get(self.url, data)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        next = soup.find("li", class_="govuk-pagination__item")
        link = next.find("a").get("href")
        self.assertEqual("/search?page=1&postcode=PE30&name=&categories=deb", link)

    def test_3nd_pagination_link_contains_category(self):
        data = {"postcode": "PE30", "categories": "deb", "page": "2"}

        response = self.client.get(self.url, data)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        next = soup.findAll("li", class_="govuk-pagination__item")[2]
        link = next.find("a").get("href")
        self.assertEqual("/search?page=3&postcode=PE30&name=&categories=deb", link)


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
        self.assertEqual(content, "Postcode: PE30Legal problem: Debt   Change search")


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


class MaintenanceModeTest(SimpleTestCase):
    client = Client()
    url = reverse("search")

    data = {"name": "foo", "categories": ["deb", "edu"]}

    maintenance_mode_h1 = "Sorry, the service is unavailable"

    @override_settings(FEATURE_FLAG_MAINTENANCE_MODE=True)
    def test_maintenance_mode_viewable_when_flag_set(self):
        response = self.client.get(self.url, self.data)
        self.assertContains(response, self.maintenance_mode_h1)

    @override_settings(FEATURE_FLAG_MAINTENANCE_MODE=False)
    def test_maintenance_mode_hidden_when_flag_unset(self):
        response = self.client.get(self.url, self.data)
        self.assertNotContains(response, self.maintenance_mode_h1)


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
        self.assertEqual(content, "Organisation: fooLegal problem: Debt, Education   Change search")


class ResultsPageWhenCategoryIsFamily(SimpleTestCase):
    client = Client()
    url = reverse("search")

    def test_results_for_exit_button_when_tailored_results(self):
        self.data = {"tailored_results": "true", "postcode": "SE11", "categories": ["mat"]}
        response = self.client.get(self.url, self.data)
        self.assertContains(response, "Exit this page")

    def test_results_for_exit_button_without_tailored_results(self):
        self.data = {"postcode": "SE11", "categories": ["mat", "hlpas"]}
        response = self.client.get(self.url, self.data)
        self.assertContains(response, "Exit this page")

    def test_results_for_no_exit_button_when_tailored_results(self):
        self.data = {"tailored_results": "true", "postcode": "SE11", "categories": ["com"]}
        response = self.client.get(self.url, self.data)
        self.assertNotContains(response, "Exit this page")

    def test_results_for_no_exit_button_without_tailored_results(self):
        self.data = {"postcode": "SE11", "categories": ["com", "pl"]}
        response = self.client.get(self.url, self.data)
        self.assertNotContains(response, "Exit this page")


class NewSearchViewTemplate(SimpleTestCase):
    client = Client()

    def test_template_link_and_css(self):
        response = self.client.get(reverse("adviser"))

        self.assertEqual(response.status_code, 200)

        # Ensure URL link is in response content
        self.assertContains(response, "https://www.gov.uk/check-legal-aid")

        # Ensure CSS class is in response content
        self.assertContains(response, "laa-fala__grey-box")


class NoResultsTest(SimpleTestCase):
    client = Client()

    url = reverse("search")

    response = client.get(url, {"name": "burns", "categories": "com"})

    def test_no_results(self):
        self.assertContains(self.response, "There are no results")


class AccessibilityViewTest(SimpleTestCase):
    client = Client()

    url = reverse("accessibility_statement")

    def test_shows_new_accessibility_statement(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Accessibility statement for Find a legal advisor")


class ErrorPageTest(SimpleTestCase):
    client = Client()
    url = reverse("search")

    def test_raises_404_when_page_number_does_not_exist(
        self,
    ):
        response = self.client.get(self.url, {"postcode": "SE11", "page": 500})
        self.assertEqual(response.status_code, 404)
