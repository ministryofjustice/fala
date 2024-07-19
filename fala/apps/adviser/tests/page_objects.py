class ResultsPage(object):
    def __init__(self, page):
        self._page = page

    @property
    def next_link(self):
        return self._page.locator('span.govuk-pagination__link-title:has-text(" Next")')

    @property
    def pagination_link_title(self):
        return self._page.locator("span.govuk-pagination__link-title")

    @property
    def h1(self):
        return self._page.locator("h1")

    @property
    def previous_link(self):
        return self._page.locator('span.govuk-pagination__link-title:has-text(" Previous")')


class OtherRegionPage(object):
    def __init__(self, page):
        self._page = page


class SearchPage(object):
    def __init__(self, page):
        self._page = page
