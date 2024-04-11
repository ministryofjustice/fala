class LaalaaPaginator(object):
    def __init__(self, data, page_size, window_size, current_page):
        self._data = data
        self._page_size = page_size
        self._window_size = window_size
        if current_page is None:
            self._current_page = 1
        else:
            self._current_page = current_page
        self._very_last_page = self._data['count'] // self._page_size

    @property
    def page_range(self):
        if self._current_page - self._window_size > 0:
            first_page = self._current_page - self._window_size
        else:
            first_page = 1

        return range(first_page, self._last_page_num())

    def _last_page_num(self):
        if self._current_page + self._window_size < self._very_last_page:
            return self._current_page + self._window_size
        else:
            return self._very_last_page

    def page(self, page_number):
        class LaaLaaPage(object):
            def __init__(self, page_num, last_page):
                if page_num is None:
                    self._page_num = 1
                else:
                    self._page_num = page_num
                self._last_page = last_page
            def has_previous(self):
                return self._page_num > 1
            def has_next(self):
                return self._page_num < self._last_page
            def previous_page_number(self):
                return self._page_num - 1
            def next_page_number(self):
                return self._page_num + 1

        return LaaLaaPage(page_number, self._last_page_num())
