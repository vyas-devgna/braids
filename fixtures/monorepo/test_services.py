import unittest

from services.catalog import load_catalog
from services.checkout import load_price


def timeout():
    raise TimeoutError


class ServiceTests(unittest.TestCase):
    def test_catalog_fallback(self):
        self.assertEqual(load_catalog(timeout), [])

    def test_checkout_fails_closed(self):
        with self.assertRaises(RuntimeError):
            load_price(timeout)


if __name__ == "__main__":
    unittest.main()
