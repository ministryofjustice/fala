from playwright.sync_api import expect
from fala.playwright.setup import PlaywrightTestSetup


class CrownDependenciesTest(PlaywrightTestSetup):
    def test_jersey(self):
        results_page = self.visit_results_page("JE1")
        expect(results_page.h1).to_have_text("The postcode JE1 is in Jersey")
        search_page = results_page.change_search()
        # Turns out that Jersey postcodes don't preserve the search term
        # so we can't test for it here
        expect(search_page.item_from_text("Organisation name")).to_be_visible()

    def test_scotland_with_persistant_search_and_categories(self):
        checkboxes = ["Family mediation", "Clinical Negligence"]

        results_page = self.visit_results_page("TD13", checkboxes)
        expect(results_page.item_from_text("Legal Aid in Scotland")).to_be_visible()
        search_page = results_page.change_search()

        # after switching back to the change search page, postcode and checkboxes are preserved
        expect(search_page.postcode_input_field).to_have_value("TD13")
        for checkbox in checkboxes:
            expect(search_page.checkbox_by_label(checkbox)).to_be_checked()
