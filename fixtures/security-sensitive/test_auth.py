import unittest

from auth import authorized


class AuthTests(unittest.TestCase):
    def test_rejects_missing_token(self):
        self.assertFalse(authorized("", "secret"))

    def test_accepts_exact_token(self):
        self.assertTrue(authorized("secret", "secret"))


if __name__ == "__main__":
    unittest.main()
