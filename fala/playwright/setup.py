import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright
from fala.apps.adviser.tests.page_objects import ResultsPage, OtherRegionPage, SearchPage


class PlaywrightTestSetup(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls._playwright = sync_playwright().start()
        cls._factory = cls._playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls._factory.close()
        cls._playwright.stop()
        super().tearDownClass()

    def setUp(self):
        super().setUp()
        self.browser = self._factory.new_context()

    def tearDown(self):
        self.browser.close()
        super().tearDown()

    def visit_results_page(self, postcode, checkbox_labels=None):
        if checkbox_labels is None:
            checkbox_labels = []
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}")
        page.get_by_label("Postcode").fill(postcode)
        for label in checkbox_labels:
            page.get_by_label(label).check()
        page.get_by_role("button", name="Search").click()
        if page.locator("#changeSearchButton"):
            return ResultsPage(page)
        else:
            return OtherRegionPage(page)

    def visit_results_page_with_full_search(self, postcode, organisation, checkbox_labels):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}")
        page.get_by_label("Postcode").fill(postcode)
        page.get_by_label("Organisation name").fill(organisation)
        for label in checkbox_labels:
            page.get_by_label(label).check()
        page.get_by_role("button", name="Search").click()
        if page.locator("#changeSearchButton"):
            return ResultsPage(page)
        else:
            return OtherRegionPage(page)

    def visit_search_page(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}")
        return SearchPage(page)
