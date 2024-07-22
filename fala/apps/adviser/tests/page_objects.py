class FalaPage(object):
    def __init__(self, page):
        self._page = page

    @property
    def h1(self):
        return self._page.locator("h1")

    @property
    def language_dropdown(self):
        return self._page.locator('select[class="goog-te-combo"]')

    def item_from_text(self, text):
        return self._page.get_by_text(text)

    def select_specific_page(self, page_no):
        return self._page.locator(f'a.govuk-pagination__link:has-text(" {page_no} ")')

    def change_search(self):
        self.item_from_text("Change Search").click()
        return SearchPage(self._page)


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

    @property
    def change_search_grey_box(self):
        return self._page.locator("li.govuk-body.notranslate")

    def listitem_for(self, postcode):
        return self._page.get_by_role("listitem").filter(has_text=f"Postcode: {postcode}")


class OtherRegionPage(FalaPage):
    pass


class SearchPage(FalaPage):
    @property
    def postcode_input_field(self):
        return self._page.get_by_label("Postcode")

    @property
    def organisation_input_field(self):
        return self._page.get_by_label("Organisation name")

    @property
    def search_button(self):
        return self.item_from_text("Search")

    @property
    def error_summary(self):
        return self._page.locator("css=.govuk-error-summary")

    @property
    def no_results_alert(self):
        return self._page.get_by_role("alert")

    def checkbox_by_label(self, label):
        return self._page.get_by_label(label)

    def search(self, postcode):
        self._page.locator("#id_postcode").fill(postcode)
        self._page.locator("#searchButton").click()
