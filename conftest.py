import pytest
from playwright.sync_api import sync_playwright
from django.test import LiveServerTestCase


class TestConfig:
    @pytest.fixture(scope="session")
    def live_server():
        server = LiveServerTestCase()
        server.setUpClass()
        yield server
        server.tearDownClass()

    @pytest.fixture(scope="session")
    def playwright():
        # sync_playwright() initialises playwright and allows it to run synchronously.
        # we need to run it synchonously so it will work with the (synchronous) pytest framework.
        # playwright is async by default
        with sync_playwright() as playwright_lifecycle:
            yield playwright_lifecycle

    @pytest.fixture(scope="session")
    def browser(playwright):
        # launch the browser
        browser = playwright.chromium.launch(headless=True)  # Set headless to False if you want to see the browser
        yield browser
        browser.close()

    @pytest.fixture(scope="function")
    def context(browser):
        context = browser.new_context()
        yield context
        context.close()

    @pytest.fixture(scope="function")
    def page(context):
        page = context.new_page()
        yield page
        page.close()
