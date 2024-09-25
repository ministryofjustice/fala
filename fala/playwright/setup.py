import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright
from fala.apps.adviser.tests.page_objects import ResultsPage, OtherRegionPage, SearchPage, CookiesPage
import pathlib
import datetime


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

        # Initialise the page object, in order to store the current page object whenever a new page is created
        self._page = None

    def tearDown(self):
        self.browser.close()
        super().tearDown()

    def take_screenshot(self):
        # make a directory to store screenshot locally
        screenshot_dir = pathlib.Path("fala/playwright/screenshots")
        screenshot_dir.mkdir(exist_ok=True)

        # name screenshots appropriately with date & time
        test_name = self._testMethodName
        timestamp = datetime.datetime.now().strftime("%d-%-m-%Y %H:%M:%S")
        screenshot_path = screenshot_dir / f"{test_name}_{timestamp}.png"

        # call playwright `screenshot` method, and take full page screenshot
        self._page.screenshot(path=str(screenshot_path), full_page=True)

    def visit_results_page(self, postcode, checkbox_labels=None):
        if checkbox_labels is None:
            checkbox_labels = []
        self._page = self.browser.new_page()
        self._page.goto(f"{self.live_server_url}")
        self._page.get_by_label("Postcode").fill(postcode)
        for label in checkbox_labels:
            self._page.get_by_label(label).check()
        self._page.get_by_role("button", name="Search").click()
        if self._page.locator("#changeSearchButton"):
            return ResultsPage(self._page)
        else:
            return OtherRegionPage(self._page)

    def visit_results_page_with_full_search(self, postcode, organisation, checkbox_labels):
        self._page = self.browser.new_page()
        self._page.goto(f"{self.live_server_url}")
        self._page.get_by_label("Postcode").fill(postcode)
        self._page.get_by_label("Organisation name").fill(organisation)
        for label in checkbox_labels:
            self._page.get_by_label(label).check()
        self._page.get_by_role("button", name="Search").click()
        if self._page.locator("#changeSearchButton"):
            return ResultsPage(self._page)
        else:
            return OtherRegionPage(self._page)

    def visit_search_page_with_url_params(self, url_params):
        self._page = self.browser.new_page()
        self._page.goto(f"{self.live_server_url}/?{url_params}")
        return SearchPage(self._page)

    def visit_search_page(self):
        self._page = self.browser.new_page()
        self._page.goto(f"{self.live_server_url}")
        return SearchPage(self._page)

    def visit_cookies_page_from_footer(self):
        self._page = self.browser.new_page()
        self._page.goto(f"{self.live_server_url}")
        self._page.locator("#cookies_footer_link").click()
        return CookiesPage(self._page)

    def visit_cookies_page_from_banner(self):
        self._page = self.browser.new_page()
        self._page.goto(f"{self.live_server_url}")
        self._page.locator("#cookies_banner_view_link").click()
        return CookiesPage(self._page)
