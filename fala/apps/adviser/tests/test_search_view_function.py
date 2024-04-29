import bs4
from django.test import SimpleTestCase, Client, override_settings
from django.urls import reverse


@override_settings(FEATURE_FLAG_NO_MAP=True)
class SearchViewFunctionTest(SimpleTestCase):
    client = Client()

    url = reverse("search")

    def test_invalid_postcode_generates_error(self):
        response = self.client.get(self.url, {"postcode": "ZZZ"})
        self.assertEqual({"postcode": ["Postcode not found"]}, response.context_data["form"].errors)


@override_settings(FEATURE_FLAG_NO_MAP=True)
class ResultsPageWithBothOrgAndPostcodeTest(SimpleTestCase):
    client = Client()
    url = reverse("search")

    data = {"postcode": "pe30", "name": "bu", "categories": "deb"}

    def test_category_search_has_just_user_input(self):
        response = self.client.get(self.url, self.data)
        self.assertContains(response, "pe30")

    def test_category_search_heading_closeness_and_matching(self):
        response = self.client.get(self.url, self.data)
        expected = (
            '<span class="results-header"> <span class="govuk-!-font-weight-bold">21 results</span> in order of closeness to'
            + '<strong class="notranslate" translate="no">pe30</strong>'
            + "matching <strong>bu</strong>."
            + "</span>"
        )
        self.assertContains(
            response,
            expected,
            html=True,
        )

    def test_search_returns_results_list(self):
        response = self.client.get(self.url, self.data)
        soup = bs4.BeautifulSoup(response.content)
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

    def test_category_search_heading(self):
        response = self.client.get(self.url, self.data)
        self.assertContains(
            response,
            '<span class="results-header"><span class="govuk-!-font-weight-bold">358 results</span> in order of closeness to'
            + '<strong class="notranslate" translate="no">PE30</strong> . </span>',
            html=True,
        )


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
