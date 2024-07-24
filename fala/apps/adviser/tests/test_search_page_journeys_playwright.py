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

    def test_full_search_journey(self):
        page = self.visit_results_page_with_full_search(
            "SE11", "Islington Law Centre", ["Housing Loss Prevention Advice Service"]
        )
        expect(page.h1).to_have_text("Search results")
        # this selector matches multiple things so picking out the 2nd one in the list.
        expect(page.change_search_grey_box.nth(1)).to_have_text("Organisation: Islington Law Centre")

    def test_no_results_journey(self):
        page = self.visit_search_page()
        page.organisation_input_field.fill("Test")
        page.search_button.click()
        expect(page.no_results_alert).to_be_visible()

    def test_invalid_organisation_search(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}")
        expect(page.locator("h1")).to_have_text("Find a legal aid adviser or family mediator")
        page.get_by_label("Organisation name").fill("test")
        page.get_by_role("button", name="Search").click()
        expect(page.locator("h1")).to_have_text("Search results")

    def test_invalid_postcode_journey(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}")
        expect(page.locator("h1")).to_have_text("Find a legal aid adviser or family mediator")
        page.get_by_label("Postcode").fill("ZZZ1")
        page.get_by_role("button", name="Search").click()
        expect(page.locator("h1")).to_have_text("Find a legal aid adviser or family mediator")
        expect(page.locator("css=.govuk-error-summary")).to_be_visible()
