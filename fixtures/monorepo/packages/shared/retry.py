def retry(operation, attempts=3, default=None):
    for _ in range(attempts):
        try:
            return operation()
        except TimeoutError:
            pass
    return default
