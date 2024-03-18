from textwrap import indent

from V3.Account import Account
from V3.fake_crypto import PublicKey


class Ledger:

    def __init__(self):
        self._accounts: dict[str, Account] = {}  # PublicKey.key -> Account.

    def __str__(self):
        result = 'Ledger contains the following accounts: \n'
        for account in self._accounts.values():
            result += f'- {account.public_key.owner}\n'
            result += indent(account.__str__(), '\t')

        return result

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
