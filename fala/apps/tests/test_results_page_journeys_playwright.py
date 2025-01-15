from playwright.sync_api import expect
from fala.playwright.setup import PlaywrightTestSetup


class ResultPageEndToEndJourneys(PlaywrightTestSetup):
    def test_change_search(self):
        results_page = self.visit_results_page(postcode="SE11")
        expect(results_page.change_search_grey_box).to_have_text("Postcode: SE11")
        search_page = results_page.change_search()
        expect(search_page.h1).to_have_text("Find a legal aid adviser or family mediator")

    def test_pagination_does_not_appear_when_there_is_one_page(self):
        results_page = self.visit_results_page(postcode="W1J5BF", organisation="charles")
        expect(results_page.pagination_link_title).not_to_be_visible()

    def test_pagination_does_appears_when_there_is_more_than_one_page(self):
        results_page = self.visit_results_page(postcode="SE11")
        expect(results_page.pagination_link_title).to_be_visible()
