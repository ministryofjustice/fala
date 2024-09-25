from playwright.sync_api import expect
from fala.playwright.setup import PlaywrightTestSetup


class TranslationSelection(PlaywrightTestSetup):

    def test_translate_to_welsh(self):
        try:
            page = self.visit_search_page()
            page.language_dropdown.select_option(label="Welsh")
            expect(page.h1).to_have_text("Dewch o hyd i gynghorydd cymorth cyfreithiol neu gyfryngwr teuluol")
            page.search("SA31 3DP")
            # this tests that the language selection persists to the results page
            expect(page.h1).to_have_text("Canlyniadau chwilio")
            page.select_page_number(4).click()
            # this tests that the language selection persists when pagination buttons are clicked
            expect(page.h1).to_have_text("Canlyniadau chwilio")

        except Exception as e:
            self.take_screenshot()
            raise e

    def test_translate_to_irish(self):
        try:
            page = self.visit_search_page()
            # searching for the value of the dropdown, as 'Irish Gaelic' text, is not being found when running test on circleCi
            page.language_dropdown.select_option(value="ga")
            expect(page.h1).to_have_text("Aimsigh comhairleoir um chúnamh dlíthiúil nó idirghabhálaí teaghlaigh")

        except Exception as e:
            self.take_screenshot()
            raise e

    def test_translate_to_scots(self):
        try:
            page = self.visit_search_page()
            page.language_dropdown.select_option(label="Scots Gaelic")
            expect(page.h1).to_have_text("Lorg comhairliche taic laghail no eadar-mheadhanair teaghlaich")

        except Exception as e:
            self.take_screenshot()
            raise e
