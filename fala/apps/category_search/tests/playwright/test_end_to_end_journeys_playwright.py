from playwright.sync_api import expect
from fala.common.test_utils.playwright.setup import PlaywrightTestSetup


class EndToEndJourneys(PlaywrightTestSetup):
    hlpas_front_page_heading = "Find a legal aid adviser for the Housing Loss Prevention Advice Service"
    med_front_page_heading = "Find a legal aid adviser for clinical negligence"
    mat_front_page_heading = "Find a legal aid adviser for family"

    def test_landing_page_with_hlpas(self):
        page = self.visit_category_search_page("?categories=hlpas")
        expect(page.h1).to_have_text(f"{self.hlpas_front_page_heading}")
        expect(page.exit_button).to_be_hidden()

    def test_landing_page_with_med(self):
        page = self.visit_category_search_page("?categories=med")
        expect(page.h1).to_have_text(f"{self.med_front_page_heading}")
        expect(page.exit_button).to_be_hidden()

    def test_landing_page_with_mat(self):
        page = self.visit_category_search_page("?categories=mat")
        expect(page.h1).to_have_text(f"{self.mat_front_page_heading}")
        expect(page.exit_button).to_be_visible()

    def test_postcode_search_journey(self):
        test_cases = [
            "SW1H 9AJ",
            "SE11",
        ]
        for postcode in test_cases:
            with self.subTest(postcode=postcode):
                page = self.visit_results_page(postcode=postcode)
                expect(page.h1).to_have_text("Your nearest legal aid advisors")

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
                page.goto(f"{self.live_server_url}/check?categories=hlpas")
                expect(page.locator("h1")).to_have_text(f"{self.hlpas_front_page_heading}")
                page.get_by_label("Postcode").fill(f"{postcode}")
                page.get_by_role("button", name="Search").click()
                expect(page.locator("h1")).to_have_text(f"{self.hlpas_front_page_heading}")
                expect(page.locator("css=.govuk-error-summary")).to_be_visible()
                page.goto(f"{self.live_server_url}/check?categories=med")
                expect(page.locator("h1")).to_have_text(f"{self.med_front_page_heading}")
                page.get_by_label("Postcode").fill(f"{postcode}")
                page.get_by_role("button", name="Search").click()
                expect(page.locator("h1")).to_have_text(f"{self.med_front_page_heading}")
                expect(page.locator("css=.govuk-error-summary")).to_be_visible()
