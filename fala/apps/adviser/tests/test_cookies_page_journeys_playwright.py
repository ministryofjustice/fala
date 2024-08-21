from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect
from fala.playwright.setup import PlaywrightTestSetup


class CookiesPageEndToEndJourneys(PlaywrightTestSetup):
    def test_cookies_page_view_accesed_from_footer(self):
        page = self.visit_cookies_page_from_footer()
        expect(page.h1).to_have_text("Cookies")

    def test_cookies_page_view_accesed_from_banner(self):
        page = self.visit_cookies_page_from_banner()
        expect(page.h1).to_have_text("Cookies")


class CookiesPageEndToEndJourneysWithFreshSetUp(StaticLiveServerTestCase):
    def test_that_cookie_has_appropriate_value(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto(f"{self.live_server_url}")
            page.wait_for_load_state(state="domcontentloaded")

            banner_text = "Cookies on Find a legal adviser or family mediator"

            # check there are no cookies
            my_cookies = context.cookies()
            for cookie in my_cookies:
                print(f"Name: {cookie['name']}, Value: {cookie['value']}")
            assert len(my_cookies) == 0, "Cookies were found, which is surprising"

            # check page shows as exected with banner showing
            expect(page.get_by_text(f"{banner_text}")).to_be_visible()
            page.locator("#cookies_footer_link").click()
            page.wait_for_load_state(state="domcontentloaded")
            expect(page.locator("h1")).to_have_text("Cookies")
            expect(page.get_by_text(f"{banner_text}")).to_be_visible()

            # check that banner disappers, once cookies allowed in banner
            page.get_by_text("Accept analytics cookies", exact=True).click()
            # using `wait_for_selector` for this assertion to run in cricleci
            page.wait_for_selector(f"{banner_text}", state="hidden")

            my_cookies = context.cookies()
            cookie_found = False
            for cookie in my_cookies:
                print(f"Name: {cookie['name']}, Value: {cookie['value']}")
                if cookie["value"] == "Allowed":
                    cookie_found = True
                    break
            assert cookie_found, "No cookie with that value exists"

            # check there is a cookie with valid value, when rejected
            page.locator("#cookies_footer_link").click()
            page.wait_for_load_state(state="domcontentloaded")
            page.wait_for_selector(f"{banner_text}", state="hidden")
            page.get_by_text("No", exact=True).click()
            page.get_by_text("Save cookie settings").click()

            my_cookies = context.cookies()
            cookie_found = False
            for cookie in my_cookies:
                print(f"Name: {cookie['name']}, Value: {cookie['value']}")
                if cookie["value"] == "Rejected":
                    cookie_found = True
                    break
            assert cookie_found, "No cookie with that value exists"

            # check there is a cookie with valid value, when allowed
            page.locator("#cookies_footer_link").click()
            page.wait_for_load_state(state="domcontentloaded")
            page.get_by_text("Yes", exact=True).click()
            page.get_by_text("Save cookie settings").click()

            my_cookies = context.cookies()
            cookie_found = False
            for cookie in my_cookies:
                print(f"Name: {cookie['name']}, Value: {cookie['value']}")
                if cookie["value"] == "Allowed":
                    cookie_found = True
                    break
            assert cookie_found, "No cookie with that value exists"

            context.close()
            browser.close()
