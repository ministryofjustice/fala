from playwright.sync_api import expect
from fala.playwright.setup import PlaywrightTestSetup


class PaginationResults(PlaywrightTestSetup):

    def test_results_pagination(self):
        checkboxes = ["Crime"]

        page = self.visit_results_page("M25 3JF", checkboxes)
        expect(page.item_from_text("1576 results in order of closeness to M25 3JF.")).to_be_visible()
        expect(page.pagination_link_title).to_be_visible()
        page.next_link.click()
        # this tests that changing page persists the category choice by not affecting the result count
        expect(page.item_from_text("1576 results in order of closeness to M25 3JF.")).to_be_visible()
        page.select_page_number(4).click()
        expect(page.item_from_text("1576 results in order of closeness to M25 3JF.")).to_be_visible()
        page.previous_link.click()
        expect(page.item_from_text("1576 results in order of closeness to M25 3JF.")).to_be_visible()
