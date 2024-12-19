from playwright.sync_api import expect
from fala.playwright.setup import PlaywrightTestSetup


class SingleCategorySearchPageEndToEndJourneys(PlaywrightTestSetup):
    hlpas_front_page_heading = "Find a legal aid adviser for the Housing Loss Prevention Advice Service"
    med_front_page_heading = "Find a legal aid adviser for clinical negligence"

    def test_landing_page_with_hlpas(self):
        page = self.visit_single_category_search_page("?categories=hlpas")
        expect(page.h1).to_have_text(f"{self.hlpas_front_page_heading}")

    def test_landing_page_with_med(self):
        page = self.visit_single_category_search_page("?categories=med")
        expect(page.h1).to_have_text(f"{self.med_front_page_heading}")

    def test_postcode_search_journey(self):
        test_cases = [
            "SW1H 9AJ",
            "SE11",
        ]
        for postcode in test_cases:
            with self.subTest(postcode=postcode):
                page = self.visit_results_page(postcode=postcode)
                expect(page.h1).to_have_text("Search results")

    def test_invalid_postcode_journey(self):
        test_cases = [
            "ZZZ1",
            "G12 OGJKLJGK",
            "LS25 ghjkhjkh",
            "IM4 TESTTTTTTTTTTTT",
        ]
        for postcode in test_cases:
            with self.subTest(postcode=postcode):
                page = self.browser.new_page()
                page.goto(f"{self.live_server_url}/single-category-search?categories=hlpas")
                expect(page.locator("h1")).to_have_text(f"{self.hlpas_front_page_heading}")
                page.get_by_label("Postcode").fill(f"{postcode}")
                page.get_by_role("button", name="Search").click()
                expect(page.locator("h1")).to_have_text(f"{self.hlpas_front_page_heading}")
                expect(page.locator("css=.govuk-error-summary")).to_be_visible()
                page.goto(f"{self.live_server_url}/single-category-search?categories=med")
                expect(page.locator("h1")).to_have_text(f"{self.med_front_page_heading}")
                page.get_by_label("Postcode").fill(f"{postcode}")
                page.get_by_role("button", name="Search").click()
                expect(page.locator("h1")).to_have_text(f"{self.med_front_page_heading}")
                expect(page.locator("css=.govuk-error-summary")).to_be_visible()
