import json
from abc import ABC
from textwrap import indent

from Header import Header
from Ledger import Ledger
from dsl.Verification import Verification
from fake_crypto import sha, new_deterministic_hash, Signature, PublicKey, sign, PrivateKey


class Block(ABC):

    @property
    def hash(self):
        return sha(self._header)

    @property
    def is_signed(self):
        return self._signature is not None

    @property
    def previous_block(self) -> 'Block' or None:
        if self._header.previous_hash is None:
            return None

        previous_hash = self._header.previous_hash
        return Ledger().get_block(previous_hash)

    @property
    def account_public_key(self) -> str:
        block = self
        while block._header.previous_hash is not None:
            # While the block is not the genesis block.
            block = block.previous_block

        return block.data['account']

    def __init__(self, previous_block: 'Block'):
        if previous_block is None:
            previous_hash: str = new_deterministic_hash()
        elif isinstance(previous_block, Block):
            previous_hash: str = previous_block.hash
        else:
            raise Exception("previous_block must be Block or None. ")

        self._header = Header(previous_hash=previous_hash)
        self._signature: Signature or None = None
        if not hasattr(self, 'data'):
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

    def add_data(self, new_key: str, new_value: any) -> 'Block':
        if self._signature is not None:
            raise Exception("Can't add data to a signed block. ")

        self.data[new_key] = new_value
        return self

    def sign(self, private_key: PrivateKey) -> None:
        if self._signature is not None:
            raise Exception("Block already signed. ")

        if not self._on_sign_verifications():
            raise Exception("Block verification failed. ")

        self._header.hash_root = sha(self.data)
        self._signature = sign(self.hash, private_key)

    def _on_sign_verifications(self) -> bool:
        """
        Verify if all the on_sign_verifications are valid. If there is no on_sign_verifications, return True.

        :return: True if all the on_sign_verifications are valid, False otherwise.
        """

        if 'on_sign_verifications' not in self.data.keys():
            return True

        return all(
            self._on_sign_verification(on_sign_object['method_name'], on_sign_object['args'])
            for on_sign_object in self.data['on_sign_verifications']
        )

    def _on_sign_verification(self, method_name: str, args: [str]) -> bool:
        """
        Verify with the corresponding method in the Verification class if the block is valid.
        :param method_name: name of the method in the Verification class.
        :param args: arguments of the method.
        :return: True if the block is valid, False otherwise.
        """

        args = [self.data[arg] if arg in self.data.keys() else arg for arg in args]
        return Verification()[method_name](*args)

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
