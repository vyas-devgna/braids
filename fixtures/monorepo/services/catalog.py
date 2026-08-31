from packages.shared.retry import retry


def load_catalog(fetch):
    return retry(fetch, default=[])
