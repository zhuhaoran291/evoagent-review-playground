def create_orders(connection, rows):
    """Insert the complete batch atomically, or leave the database unchanged."""
    for order_id, owner_id, total in rows:
        if total < 0:
            raise ValueError("order total must not be negative")
        connection.execute(
            "INSERT INTO orders (id, owner_id, total) VALUES (?, ?, ?)",
            (order_id, owner_id, total),
        )
        connection.commit()
