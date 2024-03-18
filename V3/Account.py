from textwrap import indent

from V3.Block import Block
from V3.Chain import Chain
from V3.GenesisBlock import GenesisBlock
from V3.fake_crypto import PrivateKey, PublicKey


class Account:

    @property
    def public_key(self) -> PublicKey:
        return self._public_key

    @property
    def balance(self) -> float:
        return self._chain.balance

    def __init__(self, private_key: PrivateKey, public_key: PublicKey):
        self._private_key = private_key
        self._public_key = public_key

        genesis_block = GenesisBlock()
        genesis_block.sign(private_key=private_key)
        self._chain: Chain = Chain(genesis_block)

    def __str__(self):
        result = (
            f'Account has {len(self._chain)} blocks, '
            f'{self.balance} tokens and '
            f'{"is verified" if self.verify() else "is not verified"}:\n'
        )
        result += indent(self._chain.__str__(), '\t')

        return result

    def add_block(self, block: Block) -> None:
        # Must sign the block before use the chain function.
        if not block.is_signed:
            block.sign(private_key=self._private_key)

        if not block.verify_signature(public_key=self._public_key):
            raise Exception('Error: Block signature verification failed. ')

        self._chain.add_block(block=block, public_key=self._public_key)

    def verify(self) -> bool:
        return self._chain.verify(public_key=self._public_key)
