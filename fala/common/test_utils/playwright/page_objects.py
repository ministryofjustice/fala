class FalaPage(object):
    # used with playwright tests
    def __init__(self, page):
        self._page = page

    @property
    def h1(self):
        return self._page.locator("h1")

    @property
    def error_list(self):
        return self._page.get_by_text("There is a problem")

    @property
    def exit_button(self):
        return self._page.get_by_role("button", name="Exit this page")

    @property
    def language_dropdown(self):
        return self._page.locator('select[class="goog-te-combo"]')

    def item_from_text(self, text):
        return self._page.get_by_text(text)

    def select_page_number(self, number):
        return self._page.locator(f'a.govuk-pagination__link:has-text(" {number} ")')

    def change_search(self):
        self.item_from_text("Change Search").click()
        return SearchPage(self._page)

    def search_for_something_else(self):
        self.item_from_text("Search for something else").click()
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
        return self._page.locator("li.govuk-body")

    @property
    def result_count(self):
        return self._page.locator("#result-count-overall")


class OtherRegionPage(FalaPage):
    @property
    def back_link(self):
        return self._page.locator(".govuk-back-link")


class SearchPage(FalaPage):
    @property
    def postcode_input_field(self):
        return self._page.get_by_label("Postcode")

    @property
    def organisation_input_field(self):
        return self._page.get_by_label("Name of organisation you are looking for (optional)")

    @property
    def search_button(self):
        return self.item_from_text("Search")

    def checkbox_by_label(self, label):
        return self._page.get_by_label(label)

    def search(self, postcode):
        self._page.locator("#id_postcode").fill(postcode)
        self._page.locator("#searchButton").click()


class SingleCategorySearchPage(FalaPage):
    @property
    def postcode_input_field(self):
        return self._page.get_by_label("Postcode")

    @property
    def search_button(self):
        return self.item_from_text("Search")

    def search(self, postcode):
        self._page.locator("#id_postcode").fill(postcode)
        self._page.locator("#searchButton").click()


class CookiesPage(FalaPage):
    pass
