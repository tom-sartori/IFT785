from datetime import datetime


class Header:

    def __init__(self, previous_hash: str, timestamp: datetime, hash_root: str or None = None):
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.hash_root = hash_root
