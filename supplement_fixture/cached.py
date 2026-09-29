from pathlib import Path
from .cache import cache_root


def read_cached(name):
    root = cache_root()
    return (Path(root) / name).read_text()
