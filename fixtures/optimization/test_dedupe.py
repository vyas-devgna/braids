import unittest

from dedupe import dedupe


class DedupeTests(unittest.TestCase):
    def test_preserves_order(self):
        self.assertEqual(dedupe([3, 1, 3, 2]), [3, 1, 2])

    def test_supports_unhashable_values(self):
        self.assertEqual(dedupe([[1], [1], [2]]), [[1], [2]])


if __name__ == "__main__":
    unittest.main()
