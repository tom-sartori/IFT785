from textwrap import indent

from V2.Account import Account


class Ledger:

    def __init__(self):
        self._accounts: dict[Account, float] = {}  # Account -> Balance.

    def __str__(self):
        result = 'Ledger contains the following accounts: \n'
        for account in self._accounts:
            result += f'- {account.public_key.owner} with balance {self._accounts[account]}\n'
            result += indent(account.__str__(), '\t')

        return result

    def add_account(self, account: Account):
        self._accounts[account] = 0.0

    def get_balance(self, account: Account) -> float:
        return self._accounts[account]

    def set_balance(self, account: Account, balance: float):
        self._accounts[account] = balance
