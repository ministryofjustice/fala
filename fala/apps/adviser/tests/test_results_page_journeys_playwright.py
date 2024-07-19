from playwright.sync_api import expect
from fala.playwright.setup import PlaywrightTestSetup


class ResultPageEndToEndJourneys(PlaywrightTestSetup):
    def test_pagination(self):
        page = self.visit_results_page("SE11")
        expect(page.pagination_link_title).to_be_visible()
        page.next_link.click()
        expect(page.h1).to_have_text("Search results")
        expect(page.previous_link).to_be_visible()
