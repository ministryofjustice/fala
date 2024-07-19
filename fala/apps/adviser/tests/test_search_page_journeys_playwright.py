from playwright.sync_api import expect
from fala.playwright.setup import PlaywrightTestSetup


class SearchPageEndToEndJourneys(PlaywrightTestSetup):
    def test_landing_page(self):
        page = self.visit_search_page()
        expect(page.h1).to_have_text("Find a legal aid adviser or family mediator")

    def test_postcode_search_journey(self):
        test_cases = [
            "SW1H 9AJ",
            "SE11",
        ]
        for postcode in test_cases:
            with self.subTest(postcode=postcode):
                page = self.visit_results_page(postcode)
                expect(page.h1).to_have_text("Search results")
                expect(page.listitem_for(postcode)).to_be_visible()
                expect(page.item_from_text("in order of closeness")).to_be_visible()

    def test_invlaid_postcode_journey(self):
        page = self.redirected_to_search_page()
        expect(page.error_summary).to_be_visible()
