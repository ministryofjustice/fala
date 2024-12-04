import math


class LaaLaaPaginator(object):
    def __init__(self, count, page_size, window_size, current_page):
        self._window_size = window_size
        if current_page is None:
            self._current_page = 1
        else:
            self._current_page = current_page
        self._very_last_page = math.ceil(count / page_size)

    @property
    def page_range(self):
        return range(self._first_page_num(), self._last_page_num() + 1)

    def _first_page_num(self):
        if self._current_page > self._window_size:
            return self._current_page - self._window_size
        else:
            return 1

    def _last_page_num(self):
        if self._current_page + self._window_size < self._very_last_page:
            return self._current_page + self._window_size
        else:
            return self._very_last_page

    def current_page(self):
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

        return LaaLaaPage(self._current_page, self._last_page_num())
