import pytest
from playwright.sync_api import expect
from asgiref.sync import sync_to_async


# class TestExample():
@pytest.mark.usefixtures("live_server")
def test_check_landing_page(page, live_server):
    url = sync_to_async(live_server.url)()  # this isn't working - not happy with the combo of sync and async things
    page.goto(url)

    # Page title
    expect(page).to_have_title("Find a legal aid adviser or family mediator")

    # Page header
    expect(page.locator("h1")).to_have_text("Find a legal aid adviser or family mediator")
