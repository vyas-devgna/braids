import json
from pathlib import Path


def save(path, value):
    Path(path).write_text(json.dumps(value), encoding="utf-8")
