from textwrap import indent
from fake_crypto import PublicKey


class Ledger:
    _instance = None

    def __init__(self):
        if Ledger._instance is not None:
            raise Exception("Ledger has not been")
        Ledger._instance = self
        self._accounts: dict[str, 'Account'] = {}  # PublicKey.key -> Account.
        self._blocks: dict[str, 'Block'] = {}  # Hash -> Block

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __str__(self):
        result = 'Ledger contains the following accounts: \n'
        for account in self._accounts.values():
            result += f'- {account.public_key.owner}\n'
            result += indent(account.__str__(), '\t')

        return result

    def all_block(self):
        result = 'Ledger contains the following Blocks: \n'
        for block in self._blocks.values():
            result += f'- {block.hash}\n'
            result += indent(block.__str__(), '\t')

        print(result)

        return result

    # Method to add a block to the _blocks dictionary
    def add_block(self, block: 'Block') -> None:
        block_hash = block.hash
        if block_hash in self._blocks:
            raise Exception('Error: Block already exists in the ledger. ')
        self._blocks[block_hash] = block

    def get_block(self, hash: str) -> 'Block':
        if hash not in self._blocks:
            raise Exception('Error: Block not found in the ledger. ')
        return self._blocks[hash]



    def add_account(self, account: 'Account') -> None:
        if account.public_key in self._accounts:
            raise Exception('Error: Account already exists. ')

        if not self.verify():  # Verify the ledger before adding a new account.
            raise Exception('Error: Ledger verification failed. Can not add account. ')

        self._accounts[account.public_key.key] = account

    def get_account(self, public_key: PublicKey or str) -> 'Account':
        if isinstance(public_key, PublicKey):
            public_key = public_key.key

        if public_key not in self._accounts:
            raise Exception('Error: Account not found. ')

        return self._accounts[public_key]

    def verify(self) -> bool:
        return all(account.verify() for account in self._accounts.values())

