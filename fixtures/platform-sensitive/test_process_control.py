import unittest
from unittest.mock import patch

import process_control


class ProcessTests(unittest.TestCase):
    @patch("process_control.os.kill")
    def test_posix_termination(self, kill):
        process_control.terminate(42)
        kill.assert_called_once_with(42, process_control.signal.SIGTERM)


if __name__ == "__main__":
    unittest.main()
