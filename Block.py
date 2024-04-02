import json
from abc import ABC, abstractmethod
from textwrap import indent

from Header import Header
# from Ledger import Ledger
from fake_crypto import sha, new_deterministic_hash, Signature, PublicKey, sign, PrivateKey


class Block(ABC):

    @property
    def hash(self):
        return sha(self._header)

    @property
    def is_signed(self):
        return self._signature is not None

    def account_public_key(self, ledger) -> PublicKey:
        # last_block = self.previous_block
        # while last_block._header.previous_hash is not None:
        #     last_block = last_block.previous_block
        # return last_block.account
        return ledger.account_public_key(self)


    # @property
    # def previous_block(self):
    #     return self.previous_block_by_hash(self._header.previous_hash)

    def __init__(self, previous_block: 'Block'):
        if previous_block is None:
            previous_hash: str = new_deterministic_hash()
        elif isinstance(previous_block, Block):
            previous_hash: str = previous_block.hash
        else:
            raise Exception("previous_block must be Block or None. ")

        # self._ledger: Ledger = Ledger()
        self._header = Header(previous_hash=previous_hash)
        self._signature: Signature or None = None
        self.data = dict()
        self.add_data('block_type', type(self).__name__)

    def __str__(self):
        result = ''
        result += f'previous hash: {self._header.previous_hash}\n'
        result += f'hash:          {self.hash}\n'
        result += f'timestamp:     {self._header.timestamp}\n'
        result += f'signed by:     {self._signature.signer if self.is_signed else "not yet signed"}\n'
        result += f'data:\n' + indent(json.dumps(self.data, indent=4), '\t') + '\n'
        return result

    # def previous_block_by_hash(self, hash: str):
    #
    #     pass

    def add_data(self, new_key: str, new_value: any) -> 'Block':
        if self._signature is not None:
            raise Exception("Can't add data to a signed block. ")

        self.data[new_key] = new_value
        return self

    def sign(self, private_key: PrivateKey) -> None:
        if self._signature is not None:
            raise Exception("Block already signed. ")

        if not self.on_sign_verification():
            raise Exception("Block verification failed. ")

        self._header.hash_root = sha(self.data)
        self._signature = sign(self.hash, private_key)

    @abstractmethod
    def on_sign_verification(self) -> bool:
        pass

    def verify(self, public_key: PublicKey) -> bool:
        return (self.is_signed and
                self.verify_signature(public_key) and
                self._header.hash_root == sha(self.data))

    def verify_signature(self, public_key: PublicKey) -> bool:
        if self._signature is None:
            return False

        return self._signature.verify(self.hash, public_key)

    def is_previous_of(self, next_block: 'Block') -> bool:
        return self.hash == next_block._header.previous_hash
