from django.test import SimpleTestCase, Client, override_settings
from django.urls import reverse
from fala.common.test_utils.helpers import parse_html, find_element


class ResultsPageWithBothOrgAndPostcodeTest(SimpleTestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("results")
        self.data = {"postcode": "pe30", "name": "bu", "categories": "mat"}
        self.response = self.client.get(self.url, self.data)
        self.html = parse_html(self.response.content)

    def test_category_search_has_just_user_input(self):
        self.assertContains(self.response, "PE30")

    def test_category_search_heading_closeness_and_matching_postcode_and_organisation(self):
        results_header = find_element(self.html, "span", "results-header")
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

    def test_search_parameters_box_is_visible(self):
        search_params_box = find_element(self.html, "div", "laa-fala__grey-box")
        self.assertIsNotNone(search_params_box)

    def test_search_returns_results_list(self):
        results = self.html.find_all("li", class_="results-list-item")
        self.assertEqual(10, len(results))

    def test_category_search_has_next_button(self):
        self.assertContains(self.response, '<div class="govuk-pagination__next">')

    def test_category_search_has_no_previous_button(self):
        self.assertNotContains(self.response, '<div class="govuk-pagination__previous">')

    def test_back_link_is_not_visible(self):
        back_link = find_element(self.html, "a", "laa-fala__back-link")
        self.assertIsNone(back_link)


class ResultsPageWithJustOrgTest(SimpleTestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("results")
        self.data = {"name": "foo", "categories": ["deb", "edu"]}
        self.response = self.client.get(self.url, self.data)
        self.html = parse_html(self.response.content)

    def test_search_parameters_box_contains_only_organisation_and_categories(self):
        search_params_box = find_element(self.html, "div", "laa-fala__grey-box")
        # replace the spaces in the HTML for ease of comparison
        content = search_params_box.text.replace("\n", "")
        self.assertEqual(content, "Organisation: fooLegal problem: Debt, Education Search for something else")


class ResultsPageWithJustPostcodeTest(SimpleTestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("results")
        self.data = {"postcode": "PE30", "categories": "deb"}
        self.response = self.client.get(self.url, self.data)
        self.html = parse_html(self.response.content)

    def test_category_search_heading_postcode_only(self):
        results_header = find_element(self.html, "span", "results-header")
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

    def test_search_parameters_box_contains_only_postcode_and_categories(self):
        search_params_box = find_element(self.html, "div", "laa-fala__grey-box")
        # replace the spaces in the HTML for ease of comparison
        content = search_params_box.text.replace("\n", "")
        self.assertEqual(content, "Postcode: PE30Legal problem: Debt Search for something else")


class ResultsPageWhenCategoryIsFamily(SimpleTestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("results")

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


class NoResultsTest(SimpleTestCase):
    client = Client()

    url = reverse("results")

    response = client.get(url, {"name": "burns", "categories": "com"})

    def test_no_results(self):
        self.assertContains(self.response, "There are no results")


class PaginationTest(SimpleTestCase):
    client = Client()
    url = reverse("results")

    def test_prev_pagination_link_contains_category(self):
        data = {"postcode": "PE30", "categories": "deb", "page": "2"}

        response = self.client.get(self.url, data)
        html = parse_html(response.content)
        next = find_element(html, "div", "govuk-pagination__prev")
        link = next.find("a").get("href")
        self.assertEqual("/search?page=1&postcode=PE30&name=&categories=deb", link)

    def test_prev_pagination_link_with_multiple_categories(self):
        data = {"postcode": "PE30", "categories": ["deb", "aap"], "page": "2"}

        response = self.client.get(self.url, data)
        html = parse_html(response.content)
        next = find_element(html, "div", "govuk-pagination__prev")
        link = next.find("a").get("href")
        self.assertEqual("/search?page=1&postcode=PE30&name=&categories=deb&categories=aap", link)

    def test_pagination_link_without_category(self):
        data = {"postcode": "PE30", "page": "2"}

        response = self.client.get(self.url, data)
        html = parse_html(response.content)
        next = find_element(html, "div", "govuk-pagination__prev")
        link = next.find("a").get("href")
        self.assertEqual("/search?page=1&postcode=PE30&name=", link)

    def test_next_pagination_link_contains_category(self):
        data = {"postcode": "PE30", "categories": "deb", "page": "2"}

        response = self.client.get(self.url, data)
        html = parse_html(response.content)

        next = find_element(html, "div", "govuk-pagination__next")
        link = next.find("a").get("href")
        self.assertEqual("/search?page=3&postcode=PE30&name=&categories=deb", link)

    def test_2nd_pagination_link_contains_category(self):
        data = {"postcode": "PE30", "categories": "deb", "page": "2"}

        response = self.client.get(self.url, data)
        html = parse_html(response.content)
        next = find_element(html, "li", "govuk-pagination__item")
        link = next.find("a").get("href")
        self.assertEqual("/search?page=1&postcode=PE30&name=&categories=deb", link)

    def test_3nd_pagination_link_contains_category(self):
        data = {"postcode": "PE30", "categories": "deb", "page": "2"}

        response = self.client.get(self.url, data)
        html = parse_html(response.content)
        next = html.findAll("li", class_="govuk-pagination__item")[2]
        link = next.find("a").get("href")
        self.assertEqual("/search?page=3&postcode=PE30&name=&categories=deb", link)


class ResearchBannerTest(SimpleTestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("results")
        self.data = {"name": "foo", "categories": ["deb", "edu"]}
        self.research_message = "Help improve this legal adviser search"

    @override_settings(FEATURE_FLAG_SURVEY_MONKEY=True)
    def test_research_banner_present_when_flag_set(self):
        response = self.client.get(self.url, self.data)
        self.assertContains(response, self.research_message)

    @override_settings(FEATURE_FLAG_SURVEY_MONKEY=False)
    def test_research_banner_absent_when_flag_unset(self):
        response = self.client.get(self.url, self.data)
        self.assertNotContains(response, self.research_message)
