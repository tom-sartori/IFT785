from datetime import datetime

from Header import Header
from fake_crypto import new_deterministic_hash, sha, Signature, sign, PrivateKey, PublicKey, verify


class Block:  # TODO: ABC.

    def __init__(self, previous_block: 'Block' or None = None):
        if previous_block is None:
            previous_hash: str = new_deterministic_hash()
        elif isinstance(previous_block, Block):
            previous_hash: str = previous_block.hash
        else:
            raise Exception("previous_block must be GenericBlock or None. ")

        self._signature: Signature or None = None
        self._data = dict()  # TODO: Remove this. Data is None at this point.
        self._header = Header(previous_hash, datetime.now(), sha(self._data))

    @property
    def header(self):
        return self._header

    @property
    def hash(self) -> str:
        return sha(self.header)

    @property
    def data(self, key: str or None = None) -> dict:
        return self._data if key is None else self._data[key]

    def __str__(self) -> str:
        rop = ""
        rop += f"hash:          {self.hash}\n"
        rop += f"previous hash: {self.header.previous_hash}\n"
        rop += f"timestamp:     {self.header.timestamp}\n"
        if self._signature is None:
            rop += f"not yet signed\n"
        else:
            rop += f"signed by:     {self._signature.signer}\n"
        return rop

    def __repr__(self) -> str:
        return f"<{type(self).__name__} [{self.hash}]>"

    def add_data(self, new_key: str, new_value) -> None:
        if self._signature is not None:
            raise Exception("Can't add data to a signed block. ")

        if new_key is None:
            raise Exception("'None' can't be used as data key. ")

        self._data[new_key] = new_value
        self.header.hash_root = sha(self._data)

    def sign(self, private_key: PrivateKey):
        self._signature = sign(self.hash, private_key)

    def verify_signature(self, public_key: PublicKey) -> bool:
        if self._signature is None:
            print(f'Error: Block must be signed before verification.')
            return False
        else:
            return verify(self.hash, self._signature, public_key)

    def verify_data(self) -> bool:
        return self.header.hash_root == sha(self._data)
