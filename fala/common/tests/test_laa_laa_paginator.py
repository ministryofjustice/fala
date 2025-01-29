from django.test import SimpleTestCase

from fala.common.laa_laa_paginator import LaaLaaPaginator


class LaaLaaPaginatorTest(SimpleTestCase):
    def test_short_data_has_one_page(self):
        pag = LaaLaaPaginator(count=5, page_size=10, window_size=3, current_page=1)
        self.assertEqual(1, len(pag.page_range))

    def test_short_data_has_no_previous(self):
        pag = LaaLaaPaginator(count=5, page_size=10, window_size=3, current_page=1).current_page()
        self.assertFalse(pag.has_previous())

    def test_short_data_has_no_next(self):
        pag = LaaLaaPaginator(count=5, page_size=10, window_size=3, current_page=1).current_page()
        self.assertFalse(pag.has_next())

    def test_medium_data_has_two_pages(self):
        pag = LaaLaaPaginator(count=15, page_size=10, window_size=3, current_page=1)
        self.assertEqual(2, len(pag.page_range))

    def test_medium_data_page_1_paginates(self):
        page_1 = LaaLaaPaginator(count=15, page_size=10, window_size=3, current_page=1).current_page()
        self.assertEqual([False, True], [page_1.has_previous(), page_1.has_next()])

    def test_medium_data_page_2_paginates(self):
        page_2 = LaaLaaPaginator(count=15, page_size=10, window_size=3, current_page=2).current_page()
        self.assertEqual([True, False], [page_2.has_previous(), page_2.has_next()])

    def test_large_data_has_correct_pages(self):
        pag = LaaLaaPaginator(count=105, page_size=10, window_size=2, current_page=1)
        self.assertEqual(range(1, 4), pag.page_range)

    def test_large_data_page_2_pages(self):
        pag = LaaLaaPaginator(count=105, page_size=10, window_size=2, current_page=2)
        self.assertEqual(range(1, 5), pag.page_range)

    def test_large_data_page_3_pages(self):
        pag = LaaLaaPaginator(count=105, page_size=10, window_size=2, current_page=3)
        self.assertEqual(range(1, 6), pag.page_range)

    def test_large_data_page_5_pages(self):
        pag = LaaLaaPaginator(count=105, page_size=10, window_size=2, current_page=5)
        self.assertEqual(range(3, 8), pag.page_range)
