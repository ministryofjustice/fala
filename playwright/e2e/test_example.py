import pytest
import os
from playwright.sync_api import Page, expect, sync_playwright

# This is not best practice, reconfigure when writing new playwright tests.
FALA_URL = os.environ.get("FALA_URL", "http://127.0.0.1:8000/")


# This document is a simple playwright test file and should not be treated as a standard.
# As part of EL-1480 a simple test is needed to prove Playwright works correctly.
# Future FALA tickets to create correct playwright tests will come later.
# Delete this example document when writing new playwright tickets and structure correctly.
@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


def test_check_landing_page(page: Page):
    page.goto(f"{FALA_URL}")

    # Page title
    expect(page).to_have_title("Find a legal aid adviser or family mediator")

    # Page header
    expect(page.locator("h1")).to_have_text("Find a legal aid adviser or family mediator")
