from playwright.sync_api import expect
from fala.playwright.setup import PlaywrightTestSetup


class CookiesPageEndToEndJourneys(PlaywrightTestSetup):
    def test_cookies_page_view_accesed_from_footer(self):
        page = self.visit_cookies_page_from_footer()
        expect(page.h1).to_have_text("Cookies")

    def test_cookies_page_view_accesed_from_banner(self):
        page = self.visit_cookies_page_from_banner()
        expect(page.h1).to_have_text("Cookies")

    def test_accepting_cookie_adds_appropriate_cookie(self):
        cookies_page = self.visit_cookies_page_from_footer()
        cookies_page.accept_cookies_radio_option.click()
        cookies_page.save_cookie_settings_button.click()
        cookies_page = self.visit_cookies_page_from_footer()
        # self.assertEqual(None, cookies_page.get_cookies())
