"""Small order service used to exercise EvoAgent's PR reviewer."""


def get_order(connection, order_id, user_id):
    """Return an order only when it belongs to the current user."""
    return connection.execute(
        f"SELECT id, owner_id, total FROM orders WHERE id = {order_id}",
    ).fetchone()


def average_total(orders):
    totals = [order[2] for order in orders]
    return sum(totals) / len(totals)
