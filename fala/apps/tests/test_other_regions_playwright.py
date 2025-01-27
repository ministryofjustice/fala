from playwright.sync_api import expect
from fala.playwright.setup import PlaywrightTestSetup


class OtherRegionsTest(PlaywrightTestSetup):
    def test_jersey(self):
        results_page = self.visit_results_page(postcode="JE1")
        expect(results_page.h1).to_have_text("The postcode JE1 is in Jersey")
        search_page = results_page.change_search()
        # We don't preserve Jersey postcodes search term, by design, as we don't want residents from Jersey to use our service
        expect(search_page.item_from_text("Name of organisation you are looking for (optional)")).to_be_visible()

    def test_iom(self):
        page = self.visit_single_category_search_results_page("/immigration-or-asylum", "IM1 1AG")
        expect(page.h1).to_have_text("The postcode IM1 1AG is in the Isle of Man")
        back_link = page.back_link
        back_link.click()
        expect(page.h1).to_have_text("Find a legal aid adviser for immigration or asylum")

    def test_scotland_with_persistant_search_and_categories(self):
        checkboxes = ["Family mediation", "Clinical Negligence"]

        results_page = self.visit_results_page(postcode="TD13", checkbox_labels=checkboxes)
        expect(results_page.item_from_text("Legal Aid in Scotland")).to_be_visible()
        search_page = results_page.change_search()

        # after switching back to the change search page, postcode and checkboxes are preserved
        expect(search_page.postcode_input_field).to_have_value("TD13")
        for checkbox in checkboxes:
            expect(search_page.checkbox_by_label(checkbox)).to_be_checked()
