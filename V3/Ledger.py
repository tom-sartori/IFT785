from textwrap import indent

from V3.Account import Account
from V3.fake_crypto import PublicKey


class Ledger:

    def __init__(self):
        self._accounts: dict[PublicKey, Account] = {}  # PublicKey -> Account.

    def __str__(self):
        result = 'Ledger contains the following accounts: \n'
        for public_key, account in self._accounts.items():
            result += f'- {public_key.owner}\n'
            result += indent(account.__str__(), '\t')

        return result

    def add_account(self, account: Account) -> None:
        if account.public_key in self._accounts:
            raise Exception('Error: Account already exists. ')

        self._accounts[account.public_key] = account

    def get_account(self, public_key: PublicKey) -> Account:
        return self._accounts[public_key]
