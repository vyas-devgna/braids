import hmac


def authorized(supplied_token, expected_token):
    if not supplied_token or not expected_token:
        return False
    return hmac.compare_digest(supplied_token, expected_token)
