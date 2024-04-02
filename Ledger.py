from textwrap import indent
from typing import Callable, Any

from Account import Account
from Block import Block
from GenesisBlock import GenesisBlock
from fake_crypto import PublicKey


class Ledger:

    def __init__(self):
        self._accounts: dict[str, Account] = {}  # PublicKey.key -> Account.
        self._blocks: dict[str, Block] = {}  # Hash -> Block

    def __str__(self):
        result = 'Ledger contains the following accounts: \n'
        for account in self._accounts.values():
            result += f'- {account.public_key.owner}\n'
            result += indent(account.__str__(), '\t')

        return result

    # Method to add a block to the _blocks dictionary
    def add_block(self, block: Block) -> None:
        block_hash = block.hash
        if block_hash in self._blocks:
            raise Exception('Error: Block already exists in the ledger. ')
        self._blocks[block_hash] = block

    def get_block(self, hash: str):
        if hash not in self._blocks:
            raise Exception('Error: Block not found in the ledger. ')
        return self._blocks[hash]

    # Method to get previous block from given block
    def previous_block(self, block: Block) -> Block:
        previous_hash = block._header.previous_hash
        return self.get_block(previous_hash)

    # Method to obtain the public key of the account associated with a block
    def account_public_key(self, block: Block) -> Callable[[Any], PublicKey]:
        while block._header.previous_hash is not None:
            block = self.previous_block(block)
        if isinstance(block, GenesisBlock):
            return block.account_public_key


    def add_account(self, account: Account) -> None:
        if account.public_key in self._accounts:
            raise Exception('Error: Account already exists. ')

        if not self.verify():  # Verify the ledger before adding a new account.
            raise Exception('Error: Ledger verification failed. Can not add account. ')

        self._accounts[account.public_key.key] = account

    def get_account(self, public_key: PublicKey or str) -> Account:
        if isinstance(public_key, PublicKey):
            public_key = public_key.key

        if public_key not in self._accounts:
            raise Exception('Error: Account not found. ')

        return self._accounts[public_key]

    def verify(self) -> bool:
        return all(account.verify() for account in self._accounts.values())
