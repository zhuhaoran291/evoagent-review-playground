import sqlite3
import unittest

from order_cache import CachedOrders


class CacheTests(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.addCleanup(self.connection.close)
        self.connection.executescript(
            "CREATE TABLE orders (id INTEGER PRIMARY KEY, owner_id INTEGER, total REAL);"
            "INSERT INTO orders VALUES (1, 101, 50.0), (2, 202, 80.0);"
        )

    def test_cold_lookup_hides_another_users_order(self):
        self.assertIsNone(CachedOrders(self.connection).get("2", 101))

    def test_warm_cache_still_enforces_order_ownership(self):
        cache = CachedOrders(self.connection)
        self.assertEqual(cache.get("2", 202), (2, 202, 80.0))
        self.assertIsNone(cache.get("2", 101))

    def test_cached_denial_does_not_hide_order_from_its_owner(self):
        cache = CachedOrders(self.connection)
        self.assertIsNone(cache.get("2", 101))
        self.assertEqual(cache.get("2", 202), (2, 202, 80.0))

    def test_same_owner_can_repeat_lookup(self):
        cache = CachedOrders(self.connection)
        self.assertEqual(cache.get("1", 101), cache.get("1", 101))

    def test_missing_order_returns_none(self):
        self.assertIsNone(CachedOrders(self.connection).get("99", 101))
