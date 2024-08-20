from playwright.sync_api import expect
from fala.playwright.setup import PlaywrightTestSetup


class SearchPageEndToEndJourneys(PlaywrightTestSetup):
    def test_landing_page(self):
        page = self.visit_search_page()
        expect(page.h1).to_have_text("Find a legal aid adviser or family mediator")

    def test_landing_page_with_url_params(self):
        page = self.visit_search_page_with_url_params("categories=hlpas")
        expect(page.h1).to_have_text("Find a legal aid adviser or family mediator")
        expect(page.error_list).not_to_be_visible()
        expect(page.checkbox_by_label("Housing Loss Prevention Advice Service")).to_be_checked()

    def test_landing_page_with_multiple_url_params(self):
        page = self.visit_search_page_with_url_params("categories=hlpas&categories=edu")
        expect(page.h1).to_have_text("Find a legal aid adviser or family mediator")
        expect(page.error_list).not_to_be_visible()
        expect(page.checkbox_by_label("Housing Loss Prevention Advice Service")).to_be_checked()
        expect(page.checkbox_by_label("Education")).to_be_checked()
        page._page.reload()
        expect(page.error_list).not_to_be_visible()
        expect(page.checkbox_by_label("Housing Loss Prevention Advice Service")).to_be_checked()
        expect(page.checkbox_by_label("Education")).to_be_checked()

    def test_postcode_search_journey(self):
        test_cases = [
            "SW1H 9AJ",
            "SE11",
        ]
        for postcode in test_cases:
            with self.subTest(postcode=postcode):
                page = self.visit_results_page(postcode)
                expect(page.h1).to_have_text("Search results")
                expect(page.change_search_grey_box.nth(0)).to_have_text(f"Postcode: {postcode}")
                expect(page.item_from_text("in order of closeness")).to_be_visible()

    def test_full_search_journey(self):
        page = self.visit_results_page_with_full_search(
            "SE11", "Islington Law Centre", ["Housing Loss Prevention Advice Service"]
        )
        expect(page.h1).to_have_text("Search results")
        # this selector matches multiple things so picking out the things we want using 'nth()'
        expect(page.change_search_grey_box.nth(0)).to_have_text("Postcode: SE11")
        expect(page.change_search_grey_box.nth(1)).to_have_text("Organisation: Islington Law Centre")
        expect(page.change_search_grey_box.nth(2)).to_have_text("Categories: Housing Loss Prevention Advice Service")

    def test_invalid_organisation_search(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}")
        expect(page.locator("h1")).to_have_text("Find a legal aid adviser or family mediator")
        page.get_by_label("Organisation name").fill("test")
        page.get_by_role("button", name="Search").click()
        expect(page.locator("h1")).to_have_text("Search results")
        expect(page.locator("#alert-heading-info")).to_have_text("No results")

    def test_invalid_postcode_journey(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}")
        expect(page.locator("h1")).to_have_text("Find a legal aid adviser or family mediator")
        page.get_by_label("Postcode").fill("ZZZ1")
        page.get_by_role("button", name="Search").click()
        expect(page.locator("h1")).to_have_text("Find a legal aid adviser or family mediator")
        expect(page.locator("css=.govuk-error-summary")).to_be_visible()
