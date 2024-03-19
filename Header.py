from datetime import datetime


class Header:

    def __init__(self, previous_hash: str, hash_root: str = None):
        self.previous_hash = previous_hash
        self.timestamp = datetime.now()
        self.hash_root = hash_root  # Can be None at this point. It will be updated when the block is signed.

    def __str__(self):
        return (
            f'previous hash: {self.previous_hash}\n'
            f'timestamp: {self.timestamp}\n'
            f'hash root: {self.hash_root}'
        )
