# import pytest
from playwright.sync_api import Page, expect


class StartPage:

    def test_check_landing_page(page: Page):
        page.goto("http://127.0.0.1:8000/")

        # Page title
        expect(page).to_have_title("Find a legal aid adviser or family mediator")

        # Page header
        expect(page.locator("h1")).to_have_text("Find a legal aid adviser or family mediator")
