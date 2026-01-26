from playwright.sync_api import expect
from fala.common.test_utils.playwright.setup import PlaywrightTestSetup


class PaginationResults(PlaywrightTestSetup):

    def test_results_pagination(self):
        checkboxes = ["Debt"]

        page = self.visit_results_page(postcode="M25 3JF", checkbox_labels=checkboxes)
        print("this is the page details", page)
        expect(page.item_from_text("results in order of closeness to M25 3JF")).to_be_visible()
        first_page_result_count = page.result_count.inner_text()
        expect(page.pagination_link_title).to_be_visible()
        page.next_link.click()
        # expect the result count of page 2 to match page 1.
        # then we know the filters are still applied.
        expect(page.result_count).to_have_text(first_page_result_count)
        page.select_page_number(4).click()
        expect(page.result_count).to_have_text(first_page_result_count)
        page.previous_link.click()
        expect(page.result_count).to_have_text(first_page_result_count)
