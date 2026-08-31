import json
import tempfile
import unittest
from pathlib import Path

from atomic_write import save_json


class AtomicWriteTests(unittest.TestCase):
    def test_replaces_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            save_json(path, {"value": 1})
            save_json(path, {"value": 2})
            self.assertEqual(json.loads(path.read_text()), {"value": 2})


if __name__ == "__main__":
    unittest.main()
