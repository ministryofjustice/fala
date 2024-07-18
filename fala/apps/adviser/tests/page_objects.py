class ResultsPage(object):
    def __init__(self, page):
        self._page = page

    def next_link(self):
        self._page.locator('span.govuk-pagination__link-title:has-text(" Next")')


class OtherRegionPage(object):
    def __init__(self, page):
        self._page = page


class SearchPage(object):
    def __init__(self, page):
        self._page = page
