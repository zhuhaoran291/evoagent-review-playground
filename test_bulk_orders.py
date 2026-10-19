import sqlite3
import unittest

from bulk_orders import create_orders


class BatchTests(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.addCleanup(self.connection.close)
        self.connection.executescript(
            "CREATE TABLE orders (id INTEGER PRIMARY KEY, owner_id INTEGER, total REAL);"
            "INSERT INTO orders VALUES (1, 101, 50.0), (2, 202, 80.0);"
        )

    def added_rows(self):
        return self.connection.execute("SELECT id FROM orders WHERE id >= 3 ORDER BY id").fetchall()

    def test_complete_valid_batch_is_saved(self):
        create_orders(self.connection, [(3, 101, 10.0), (4, 101, 20.0)])
        self.assertEqual(self.added_rows(), [(3,), (4,)])

    def test_invalid_first_row_saves_nothing(self):
        with self.assertRaises(ValueError):
            create_orders(self.connection, [(3, 101, -1.0)])
        self.assertEqual(self.added_rows(), [])

    def test_invalid_later_row_rolls_back_earlier_rows(self):
        with self.assertRaises(ValueError):
            create_orders(self.connection, [(3, 101, 10.0), (4, 101, -1.0)])
        self.assertEqual(self.added_rows(), [])

    def test_duplicate_later_row_rolls_back_earlier_rows(self):
        with self.assertRaises(sqlite3.IntegrityError):
            create_orders(self.connection, [(3, 101, 10.0), (3, 101, 20.0)])
        self.assertEqual(self.added_rows(), [])
