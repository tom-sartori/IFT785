from main.command_manager.commands.Command import Command
from main.ledger.Ledger import Ledger


class ShowAllAccountsCommand(Command):
    """
    Some commands can implement simple operations on their own.
    """

    def execute(self) -> None:
        result = 'Ledger contains the following accounts: \n'
        for account in Ledger().accounts.values():
            result += f'- {account.public_key.owner} - hash : {account.public_key.key} | hash head {account.head.hash} \n'

        print(result)
