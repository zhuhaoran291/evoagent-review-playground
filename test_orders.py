import sqlite3
import unittest

from orders import average_total, get_order


class OrderTests(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.addCleanup(self.connection.close)
        self.connection.executescript(
            "CREATE TABLE orders (id INTEGER, owner_id INTEGER, total REAL);"
            "INSERT INTO orders VALUES (1, 101, 50.0), (2, 202, 80.0);"
        )

    def test_owner_can_read_order(self):
        self.assertEqual(get_order(self.connection, "1", 101), (1, 101, 50.0))

    def test_other_users_order_is_hidden(self):
        self.assertIsNone(get_order(self.connection, "2", 101))

    def test_sql_input_is_not_executed(self):
        self.assertIsNone(get_order(self.connection, "0 OR 1=1", 101))

    def test_average_handles_empty_orders(self):
        self.assertEqual(average_total([]), 0.0)


if __name__ == "__main__":
    unittest.main()
