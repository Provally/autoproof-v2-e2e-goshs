import os
from pathlib import Path
from urllib.parse import urlparse
import socket


def cache_root():
    endpoint = urlparse(os.environ["FIXTURE_REDIS_URL"])
    with socket.create_connection((endpoint.hostname, endpoint.port or 6379), timeout=10) as client:
        client.sendall(b"*2\r\n$3\r\nGET\r\n$12\r\nfixture:root\r\n")
        stream = client.makefile("rb")
        header = stream.readline().strip()
        if not header.startswith(b"$") or int(header[1:]) < 0:
            raise RuntimeError("The optional cache fixture has not been seeded")
        return stream.read(int(header[1:])).decode()
