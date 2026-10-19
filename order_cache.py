from orders import get_order


class CachedOrders:
    """Cache order lookups while preserving the current user's visibility."""

    def __init__(self, connection):
        self.connection = connection
        self.cache = {}

    def get(self, order_id, user_id):
        key = order_id
        if key not in self.cache:
            self.cache[key] = get_order(self.connection, order_id, user_id)
        return self.cache[key]
