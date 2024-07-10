from playwright.sync_api import expect
from fala.playwright.setup import PlaywrightTestSetup


class TestEndToEndJourneys(PlaywrightTestSetup):

    def setUp(self) -> None:
        self.page = self.browser.new_page()

    def visit_search_page(self):
        self.page.goto(f"{self.live_server_url}")

    def test_landing_page(self):
        self.visit_search_page()
        expect(self.page).to_have_title("Find a legal aid adviser or family mediator")
        expect(self.page.locator("h1")).to_have_text("Find a legal aid adviser or family mediator")

    def test_postcode_search_journey(self):
        test_cases = [
            "SW1H 9AJ",
            "SE11",
        ]
        for postcode in test_cases:
            with self.subTest(postcode=postcode):
                self.visit_search_page()
                self.page.get_by_label("Postcode").fill(postcode)
                self.page.get_by_role("button", name="Search").click()
                expect(self.page.locator("h1")).to_have_text("Search results")
                expect(self.page.get_by_role("listitem").filter(has_text=f"Postcode: {postcode}")).to_be_visible()
                expect(self.page.get_by_text("in order of closeness")).to_be_visible()
