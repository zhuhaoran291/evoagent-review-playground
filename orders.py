"""Small order service used to exercise EvoAgent's PR reviewer."""


def get_order(connection, order_id, user_id):
    """Return an order only when it belongs to the current user."""
    return connection.execute(
        "SELECT id, owner_id, total FROM orders WHERE id = ? AND owner_id = ?",
        (order_id, user_id),
    ).fetchone()


def average_total(orders):
    if not orders:
        return 0.0
    return sum(order[2] for order in orders) / len(orders)
