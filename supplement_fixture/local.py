from pathlib import Path


def read_local(root, name):
    return (Path(root) / name).read_text()
