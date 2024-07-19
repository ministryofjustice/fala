class FalaPage(object):
    def __init__(self, page):
        self._page = page

    @property
    def h1(self):
        return self._page.locator("h1")

    def item_from_text(self, text):
        return self._page.get_by_text(text)


class ResultsPage(FalaPage):
    @property
    def next_link(self):
        return self._page.locator('span.govuk-pagination__link-title:has-text(" Next")')

    @property
    def pagination_link_title(self):
        return self._page.locator("span.govuk-pagination__link-title")

    @property
    def previous_link(self):
        return self._page.locator('span.govuk-pagination__link-title:has-text(" Previous")')

    def select_specific_page(self, page_no):
        return self._page.locator(f'a.govuk-pagination__link:has-text(" {page_no} ")')

    @property
    def change_search_button(self):
        return self._page.get_by_role("button", id="changeSearchButton")

    def listitem_for(self, postcode):
        return self._page.get_by_role("listitem").filter(has_text=f"Postcode: {postcode}")

    def change_search(self):
        self.item_from_text("Change Search").click()
        return SearchPage(self._page)


class OtherRegionPage(FalaPage):
    def change_search(self):
        self.item_from_text("Change Search").click()
        return SearchPage(self._page)


class SearchPage(FalaPage):
    @property
    def postcode_input_field(self):
        return self._page.get_by_label("Postcode")

    @property
    def search_button(self):
        return self._page.get_by_role("button", id="searchButton")

    @property
    def error_summary(self):
        return self._page.locator("css=.govuk-error-summary")

    def checkbox_by_label(self, label):
        return self._page.get_by_label(label)

    @property
    def language_dropdown(self):
        return self._page.locator('select[class="goog-te-combo"]')

    def select_specific_page(self, page_no):
        return self._page.locator(f'a.govuk-pagination__link:has-text(" {page_no} ")')

    def search(self, postcode):
        self._page.locator("#id_postcode").fill(postcode)
        self._page.locator("#searchButton").click()
