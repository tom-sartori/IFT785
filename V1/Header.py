from datetime import datetime


class Header:

    def __init__(self, previous_hash: str, timestamp: datetime, hash_root: str):
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.hash_root = hash_root

    def __repr__(self):
        return f"<{type(self).__name__} [{self.previous_hash}]>"
