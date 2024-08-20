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
    banner_text = "Cookies on Find a legal adviser or family mediator"

    def check_no_cookies(self, my_cookies):
        assert len(my_cookies) == 0, "Cookies were found, which is surprising"

    def verify_cookie_value(self, expected_value, my_cookies):
        cookie_found = False
        for cookie in my_cookies:
            print(f"Name: {cookie['name']}, Value: {cookie['value']}")
            if cookie["value"] == expected_value:
                cookie_found = True
                break
        assert cookie_found, f"No cookie with value '{expected_value}', exists"

    def tear_down(self, page, context):
        page.context.close()
        context.browser.close()

    def accept_cookie_from_banner(self, page):
        # check that banner disappers, once cookies accepted in banner
        # using `wait_for_selector` for this assertion to run in cricleci
        # reload page, as cookie rejected in banner and will not appear in browser until some time
        page.get_by_text("Accept analytics cookies", exact=True).click()
        page.wait_for_selector(f"{self.banner_text}", state="hidden")
        page.reload()

    def reject_cookie_from_banner(self, page):
        page.get_by_text("Reject analytics cookies", exact=True).click()
        page.wait_for_selector(f"{self.banner_text}", state="hidden")
        page.reload()

    def accept_cookie_on_policy_page(self, page):
        page.locator("#cookies_footer_link").click()
        page.wait_for_load_state(state="domcontentloaded")
        expect(page.locator("h1")).to_have_text("Cookies")
        page.get_by_text("Yes", exact=True).click()
        page.get_by_text("Save cookie settings").click()

    def reject_cookie_on_policy_page(self, page):
        page.locator("#cookies_footer_link").click()
        page.wait_for_load_state(state="domcontentloaded")
        expect(page.locator("h1")).to_have_text("Cookies")
        page.get_by_text("No", exact=True).click()
        page.get_by_text("Save cookie settings").click()

    def test_cookie_has_appropriate_value_when_accepted_in_banner(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            page.goto(f"{self.live_server_url}")
            page.wait_for_load_state(state="domcontentloaded")

            my_cookies = context.cookies()
            self.check_no_cookies(my_cookies)

            self.accept_cookie_from_banner(page)

            my_cookies = context.cookies()
            self.verify_cookie_value("Allowed", my_cookies)

            self.tear_down(page, context)

    def test_cookie_has_appropriate_value_when_rejected_in_banner(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            page.goto(f"{self.live_server_url}")
            page.wait_for_load_state(state="domcontentloaded")

            my_cookies = context.cookies()
            self.check_no_cookies(my_cookies)

            self.reject_cookie_from_banner(page)

            my_cookies = context.cookies()
            self.verify_cookie_value("Rejected", my_cookies)

            self.tear_down(page, context)

    def test_cookie_has_appropriate_value_when_accepted_on_policy_page(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            page.goto(f"{self.live_server_url}")
            page.wait_for_load_state(state="domcontentloaded")

            my_cookies = context.cookies()
            self.check_no_cookies(my_cookies)

            self.accept_cookie_on_policy_page(page)

            my_cookies = context.cookies()
            self.verify_cookie_value("Allowed", my_cookies)
            expect(page.get_by_text(f"{self.banner_text}")).to_be_hidden()

            self.tear_down(page, context)

    def test_cookie_has_appropriate_value_when_rejected_on_policy_page(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            page.goto(f"{self.live_server_url}")
            page.wait_for_load_state(state="domcontentloaded")

            my_cookies = context.cookies()
            self.check_no_cookies(my_cookies)

            self.reject_cookie_on_policy_page(page)

            my_cookies = context.cookies()
            self.verify_cookie_value("Rejected", my_cookies)
            expect(page.get_by_text(f"{self.banner_text}")).to_be_hidden()

            self.tear_down(page, context)

    def test_cookie_has_appropriate_value_across_pages(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            page.goto(f"{self.live_server_url}")
            page.wait_for_load_state(state="domcontentloaded")

            my_cookies = context.cookies()
            self.check_no_cookies(my_cookies)

            self.accept_cookie_from_banner(page)

            my_cookies = context.cookies()
            self.verify_cookie_value("Allowed", my_cookies)

            self.reject_cookie_on_policy_page(page)

            my_cookies = context.cookies()
            self.verify_cookie_value("Rejected", my_cookies)

            self.accept_cookie_on_policy_page(page)

            my_cookies = context.cookies()
            self.verify_cookie_value("Allowed", my_cookies)

            self.tear_down(page, context)
