from playwright.sync_api import expect
from fala.apps.adviser.tests.playwright.setup import PlaywrightTestSetup
from time import sleep


class TestEndToEndJourneys(PlaywrightTestSetup):
    def test_landing_page(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}")
        expect(page).to_have_title("Find a legal aid adviser or family mediator")
        expect(page.locator("h1")).to_have_text("Find a legal aid adviser or family mediator")

    def test_postcode_search_journey(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}")
        page.get_by_label("Postcode").fill("SE11")
        page.get_by_role("button", name="Search").click()
        sleep(10)
        expect(page.locator("h1")).to_have_text("Search results")
        expect(page.get_by_role("listitem").filter(has_text="Postcode: SE11")).to_be_visible()
        expect(page.get_by_text("in order of closeness")).to_be_visible()
