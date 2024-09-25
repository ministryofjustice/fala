from playwright.sync_api import expect
from fala.playwright.setup import PlaywrightTestSetup


class ResultPageEndToEndJourneys(PlaywrightTestSetup):
    def test_change_search(self):
        try:
            results_page = self.visit_results_page("SE11")
            expect(results_page.change_search_grey_box).to_have_text("Postcode: SE11")
            search_page = results_page.change_search()
            expect(search_page.h1).to_have_text("Find a legal aid adviser or family mediator")

        except Exception as e:
            self.take_screenshot()
            raise e
