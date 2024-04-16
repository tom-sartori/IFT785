from command_manager.Command import Command

from ledger.Ledger import Ledger


class ShowAllAccountsCommand(Command):
    """
    Some commands can implement simple operations on their own.
    """

    def execute(self) -> None:
        all_accounts = Ledger()._accounts
        result = 'Ledger contains the following accounts: \n'
        for account in all_accounts.values():
            result += f'- {account.public_key.owner} - {account.public_key.key}\n'

        print(result)
