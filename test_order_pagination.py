import unittest

from order_pagination import page_orders


class PaginationTests(unittest.TestCase):
    def test_first_page_starts_with_first_order(self):
        self.assertEqual(page_orders([1, 2, 3, 4, 5], 1, 2), [1, 2])

    def test_second_page_has_no_gap(self):
        self.assertEqual(page_orders([1, 2, 3, 4, 5], 2, 2), [3, 4])

    def test_last_partial_page_preserves_last_order(self):
        self.assertEqual(page_orders([1, 2, 3, 4, 5], 3, 2), [5])

    def test_empty_orders_return_empty_page(self):
        self.assertEqual(page_orders([], 1, 2), [])

    def test_out_of_range_page_is_empty(self):
        self.assertEqual(page_orders([1, 2, 3], 4, 2), [])

    def test_invalid_page_is_rejected(self):
        with self.assertRaises(ValueError):
            page_orders([1], 0, 2)
