class FalaPage(object):
    def __init__(self, page):
        self._page = page

    @property
    def h1(self):
        return self._page.locator("h1")

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

    def listitem_for(self, postcode):
        return self._page.get_by_role("listitem").filter(has_text=f"Postcode: {postcode}")

    def item_from_text(self, text):
        return self._page.get_by_text(text)

class OtherRegionPage(FalaPage):
    pass


class SearchPage(FalaPage):
    pass

