import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect
from fala.apps.adviser.tests.page_objects import ResultsPage, OtherRegionPage


class PlaywrightTestSetup(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def visit_results_page(self, postcode):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}")
        page.get_by_label("Postcode").fill(postcode)
        page.get_by_role("button", name="Search").click()
        expect(page.locator("h1")).to_have_text("Search results")
        return ResultsPage(page)

    def visit_other_region_page(self, postcode):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}")
        page.get_by_label("Postcode").fill(postcode)
        page.get_by_role("button", name="Search").click()
        expect(page.locator("p")).to_have_text("This search only covers England and Wales")
        return OtherRegionPage(page)
