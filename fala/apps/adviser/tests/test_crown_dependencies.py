from playwright.sync_api import expect
from fala.playwright.setup import PlaywrightTestSetup


class CrownDependenciesTest(PlaywrightTestSetup):
    def test_jersey(self):
        page = self.visit_results_page("JE1")
        expect(page.h1).to_have_text("The postcode JE1 is in Jersey")
