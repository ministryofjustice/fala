from playwright.sync_api import expect
from fala.playwright.setup import PlaywrightTestSetup


class ResultPageEndToEndJourneys(PlaywrightTestSetup):

    def setUp(self) -> None:
        self.page = self.browser.new_page()

    def visit_valid_uk_results_page(self):
        self.page.goto(f"{self.live_server_url}")
        self.page.get_by_label("Postcode").fill("SE11")
        self.page.get_by_role("button", name="Search").click()
        expect(self.page.locator("h1")).to_have_text("Search results")

    def test_pagination(self):
        self.visit_valid_uk_results_page()
        expect(self.page.locator("span.govuk-pagination__link-title")).to_be_visible()
        self.page.locator('span.govuk-pagination__link-title:has-text(" Next")').click()
        expect(self.page.locator("h1")).to_have_text("Search results")
        expect(self.page.locator('span.govuk-pagination__link-title:has-text(" Previous")')).to_be_visible()
