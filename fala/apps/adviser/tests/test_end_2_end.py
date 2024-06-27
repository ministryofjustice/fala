from playwright.sync_api import expect
from fala.apps.adviser.tests.playwright.setup import PlaywrightTestSetup


class TestEndToEndJourneys(PlaywrightTestSetup):
    def test_check_landing_page(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}")

        # Page title
        expect(page).to_have_title("Find a legal aid adviser or family mediator")

        # Page header
        expect(page.locator("h1")).to_have_text("Find a legal aid adviser or family mediator")
