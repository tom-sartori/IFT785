from textwrap import indent

from Block import Block
from Chain import Chain
from GenesisBlock import GenesisBlock
from fake_crypto import PrivateKey, PublicKey


class Account:

    @property
    def public_key(self) -> PublicKey:
        return self._public_key

    @property
    def head(self) -> Block:
        return self._chain.head

    @property
    def balances(self) -> dict[str, int or float]:
        return self._chain.get_balances()

    def __init__(self, private_key: PrivateKey, public_key: PublicKey):
        self._private_key = private_key
        self._public_key = public_key

        genesis_block = GenesisBlock(public_key=public_key)
        genesis_block.sign(private_key=private_key)
        self._chain: Chain = Chain(genesis_block)

    def __str__(self):
        result = ''
        result += f'Account has {len(self._chain)} blocks and '
        result += f'{"is verified" if self.verify() else "is not verified"}. \n'
        result += f'It has the following balances: {self.balances}\n'
        result += indent(self._chain.__str__(), '\t')

        return result

    def add_block(self, block: Block) -> None:
        # Must sign the block before use the chain.add_block() method.
        if not block.is_signed:
            block.sign(private_key=self._private_key)

        if not block.verify_signature(public_key=self._public_key):
            raise Exception('Error: Block signature verification failed. ')

        self._chain.add_block(block=block, public_key=self._public_key)

    def verify(self) -> bool:
        return self._chain.verify(public_key=self._public_key)
    
    def getChain(self) -> Chain:
        return self._chain
