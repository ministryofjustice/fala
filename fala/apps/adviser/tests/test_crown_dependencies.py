from playwright.sync_api import expect
from fala.playwright.setup import PlaywrightTestSetup


class CrownDependenciesTest(PlaywrightTestSetup):
    def test_jersey(self):
        results_page = self.visit_results_page("JE1")
        expect(results_page.h1).to_have_text("The postcode JE1 is in Jersey")
        search_page = results_page.change_search()
        expect(search_page.item_from_text("Organisation name")).to_be_visible()

    def test_scotland(self):
        results_page = self.visit_results_page("TD13")
        expect(results_page.item_from_text("Legal Aid in Scotland")).to_be_visible()
        search_page = results_page.change_search()
        expect(search_page.postcode_input_field).to_have_value("TD13")
