def page_orders(orders, page=1, page_size=20):
    """Return a one-based page of orders; out-of-range pages are empty."""
    if page < 1 or page_size < 1:
        raise ValueError("page and page_size must be positive")
    start = page * page_size
    return orders[start:start + page_size]
