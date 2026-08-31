import os
import signal


def terminate(pid):
    os.kill(pid, signal.SIGTERM)
