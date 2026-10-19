import unittest

from orders import average_total


class AverageContractTests(unittest.TestCase):
    def test_one_order(self):
        self.assertEqual(average_total([(1, 101, 10.0)]), 10.0)

    def test_multiple_orders(self):
        self.assertEqual(average_total([(1, 101, 10.0), (2, 101, 20.0)]), 15.0)

    def test_zero_total_is_valid(self):
        self.assertEqual(average_total([(1, 101, 0.0)]), 0.0)
