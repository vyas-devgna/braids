from packages.shared.retry import retry


def load_price(fetch):
    price = retry(fetch)
    if price is None:
        raise RuntimeError("price unavailable")
    return price
