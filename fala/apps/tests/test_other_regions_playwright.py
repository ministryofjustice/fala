from playwright.sync_api import expect
from fala.playwright.setup import PlaywrightTestSetup


class OtherRegionsTest(PlaywrightTestSetup):
    def test_jersey(self):
        page = self.visit_results_page(postcode="JE1")
        expect(page.h1).to_have_text("The postcode JE1 is in Jersey")
        back_link = page.back_link
        back_link.click()
        expect(page.h1).to_have_text("Find a legal aid adviser or family mediator")

    def test_scotland_with_persistant_search_and_categories(self):
        checkboxes = ["Family mediation", "Clinical Negligence"]

        results_page = self.visit_results_page(postcode="TD13", checkbox_labels=checkboxes)
        expect(results_page.item_from_text("Legal Aid in Scotland")).to_be_visible()
        search_page = results_page.change_search()

        # after switching back to the change search page, postcode and checkboxes are preserved
        expect(search_page.postcode_input_field).to_have_value("TD13")
        for checkbox in checkboxes:
            expect(search_page.checkbox_by_label(checkbox)).to_be_checked()
