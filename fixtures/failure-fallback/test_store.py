import json
import tempfile
import unittest
from pathlib import Path

from store import save


class StoreTests(unittest.TestCase):
    def test_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            save(path, {"ready": True})
            self.assertEqual(json.loads(path.read_text()), {"ready": True})


if __name__ == "__main__":
    unittest.main()
