from playwright.sync_api import expect
from fala.playwright.setup import PlaywrightTestSetup


class TranslationSelection(PlaywrightTestSetup):

    def test_translate_to_welsh(self):
        page = self.browser.new_page()
        page = self.visit_search_page()
        page.language_dropdown.select_option(label="Welsh")
        expect(page.h1).to_have_text("Dewch o hyd i gynghorydd cymorth cyfreithiol neu gyfryngwr teuluol")
        page.search("SA31 3DP")
        # this tests that the language selection persists to the results page
        expect(page.h1).to_have_text("Canlyniadau chwilio")
        page.select_specific_page(4).click()
        # this tests that the language selection persists when pagination buttons are clicked
        expect(page.h1).to_have_text("Canlyniadau chwilio")

    def test_translate_to_irish(self):
        page = self.browser.new_page()
        page = self.visit_search_page()
        page.language_dropdown.select_option(label="Irish Gaelic")
        expect(page.h1).to_have_text("Aimsigh comhairleoir um chúnamh dlíthiúil nó idirghabhálaí teaghlaigh")

    def test_translate_to_scots(self):
        page = self.browser.new_page()
        page = self.visit_search_page()
        page.language_dropdown.select_option(label="Scots Gaelic")
        expect(page.h1).to_have_text("Lorg comhairliche taic laghail no eadar-mheadhanair teaghlaich")
