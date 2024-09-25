from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect
from fala.playwright.setup import PlaywrightTestSetup
import pathlib
import datetime


class CookiesPageEndToEndJourneys(PlaywrightTestSetup):
    def test_cookies_page_view_accessed_from_footer(self):
        try:
            page = self.visit_cookies_page_from_footer()
            expect(page.h1).to_have_text("Cookies")
            self.test_failed_take_screenshot = False

        except Exception as e:
            self.take_screenshot()
            raise e

    def test_cookies_page_view_accessed_from_banner(self):
        try:
            page = self.visit_cookies_page_from_banner()
            expect(page.h1).to_have_text("Cookies")
            self.test_failed_take_screenshot = False

        except Exception as e:
            self.take_screenshot()
            raise e


class CookiesPageEndToEndJourneysWithFreshSetUp(StaticLiveServerTestCase):
    banner_text = "Cookies on Find a legal adviser or family mediator"

    def check_no_cookies(self, my_cookies):
        assert len(my_cookies) == 0, "Cookies were found, which is surprising"

    def verify_cookie_value(self, expected_value, my_cookies):
        cookie_found = False
        for cookie in my_cookies:
            if cookie["value"] == expected_value:
                cookie_found = True
                break
        assert cookie_found, f"No cookie with value '{expected_value}', exists"

    def tear_down(self, page, context):
        page.context.close()
        context.browser.close()

    def take_screenshot(self, page):
        screenshot_dir = pathlib.Path("fala/playwright/screenshots")
        screenshot_dir.mkdir(exist_ok=True)

        test_name = self._testMethodName
        timestamp = datetime.datetime.now().strftime("%d-%-m-%Y %H:%M:%S")
        screenshot_path = screenshot_dir / f"{test_name}_{timestamp}.png"

        page.screenshot(path=str(screenshot_path), full_page=True)

    def accept_cookie_from_banner(self, page):
        # check that banner disappears, once cookies accepted in banner
        # using `wait_for_selector` for this assertion to run in cricleci
        # reload page, as cookie rejected in banner and will not appear in browser until some time
        page.get_by_text("Accept analytics cookies", exact=True).click()
        page.wait_for_selector(f"{self.banner_text}", state="hidden", strict=True)

    def reject_cookie_from_banner(self, page):
        page.get_by_text("Reject analytics cookies", exact=True).click()
        page.wait_for_selector(f"{self.banner_text}", state="hidden", strict=True)

    def accept_cookie_on_policy_page(self, page):
        page.locator("#cookies_footer_link").click()
        page.wait_for_load_state(state="domcontentloaded")
        expect(page.locator("h1")).to_have_text("Cookies")
        page.get_by_text("Yes", exact=True).click()
        page.get_by_text("Save cookie settings").click()
        page.wait_for_selector(f"{self.banner_text}", state="hidden", strict=True)

    def reject_cookie_on_policy_page(self, page):
        page.locator("#cookies_footer_link").click()
        page.wait_for_load_state(state="domcontentloaded")
        expect(page.locator("h1")).to_have_text("Cookies")
        page.get_by_text("No", exact=True).click()
        page.get_by_text("Save cookie settings").click()
        page.wait_for_selector(f"{self.banner_text}", state="hidden", strict=True)

    def test_cookie_has_appropriate_value_when_accepted_in_banner(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            page.goto(f"{self.live_server_url}")
            page.wait_for_load_state(state="domcontentloaded")

            try:
                my_cookies = context.cookies()
                self.check_no_cookies(my_cookies)

                self.accept_cookie_from_banner(page)

                my_cookies = context.cookies()
                self.verify_cookie_value("Allowed", my_cookies)

            except Exception as e:
                self.take_screenshot(page)
                raise e

            finally:
                self.tear_down(page, context)

    def test_cookie_has_appropriate_value_when_rejected_in_banner(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            page.goto(f"{self.live_server_url}")
            page.wait_for_load_state(state="domcontentloaded")

            try:
                my_cookies = context.cookies()
                self.check_no_cookies(my_cookies)

                self.reject_cookie_from_banner(page)

                my_cookies = context.cookies()
                self.verify_cookie_value("Rejected", my_cookies)

            except Exception as e:
                self.take_screenshot(page)
                raise e

            finally:
                self.tear_down(page, context)

    def test_cookie_has_appropriate_value_when_accepted_on_policy_page(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            page.goto(f"{self.live_server_url}")
            page.wait_for_load_state(state="domcontentloaded")

            try:
                my_cookies = context.cookies()
                self.check_no_cookies(my_cookies)

                self.accept_cookie_on_policy_page(page)

                my_cookies = context.cookies()
                self.verify_cookie_value("Allowed", my_cookies)
                expect(page.get_by_text(f"{self.banner_text}")).to_be_hidden()

            except Exception as e:
                self.take_screenshot(page)
                raise e

            finally:
                self.tear_down(page, context)

    def test_cookie_has_appropriate_value_when_rejected_on_policy_page(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            page.goto(f"{self.live_server_url}")
            page.wait_for_load_state(state="domcontentloaded")

            try:
                my_cookies = context.cookies()
                self.check_no_cookies(my_cookies)

                self.reject_cookie_on_policy_page(page)

                my_cookies = context.cookies()
                self.verify_cookie_value("Rejected", my_cookies)
                expect(page.get_by_text(f"{self.banner_text}")).to_be_hidden()

            except Exception as e:
                self.take_screenshot(page)
                raise e

            finally:
                self.tear_down(page, context)

    def test_cookie_has_appropriate_value_across_pages(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            page.goto(f"{self.live_server_url}")
            page.wait_for_load_state(state="domcontentloaded")

            try:
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

            except Exception as e:
                self.take_screenshot(page)
                raise e

            finally:
                self.tear_down(page, context)
