"""Small order service used to exercise EvoAgent's PR reviewer."""


def get_order(connection, order_id, user_id):
    """Return an order only when it belongs to the current user."""
    query = "SELECT id, owner_id, total FROM orders WHERE id = ? AND owner_id = ?"
    return connection.execute(query, (order_id, user_id)).fetchone()


def average_total(orders):
    if not orders:
        return 0.0
    totals = [order[2] for order in orders]
    return sum(totals) / len(totals)
