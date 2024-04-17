from textwrap import indent

from ledger.Ledger import Ledger
from ledger.account.Chain import Chain
from ledger.block.Block import Block
from ledger.block.GenesisBlock import GenesisBlock
from utils.fake_crypto import PublicKey, PrivateKey


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

        Ledger().add_block(genesis_block)

    def __str__(self):
        result = ''
        result += f'- {self.public_key.owner} - {self.public_key.key}\n'
        result += indent(f'This account has {len(self._chain)} blocks and {"is verified" if self.verify() else "is not verified"}. \n', '\t')
        result += indent(f'It has the following balances: {self.balances}\n\n---\n', '\t')
        result += indent(self._chain.__str__(), '\t')

        return result

    def get_balance(self, unit: str):
        return self._chain.get_balance(unit)

    def add_block(self, block: Block) -> None:
        # Must sign the block before use the chain.add_block() method.
        if not block.is_signed:
            block.sign(private_key=self._private_key)

        if not block.verify_signature(public_key=self._public_key):
            raise Exception('Error: Block signature verification failed. ')

        self._chain.add_block(block=block, public_key=self._public_key)

        # Adding the block into the blocks dictionary of Ledger.
        Ledger().add_block(block)
        print("Block added successfully")

    def verify(self) -> bool:
        return self._chain.verify(public_key=self._public_key)
