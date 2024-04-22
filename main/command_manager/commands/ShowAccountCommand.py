from main.command_manager.commands.Command import Command
from main.ledger.Ledger import Ledger


class ShowAccountCommand(Command):
    """
    Some commands can implement simple operations on their own.
    """

    def __init__(self, public_key: str) -> None:
        self.public_key = public_key

    def execute(self) -> None:
        try:
            account = Ledger().get_account(str(self.public_key))
            print(account)
        except Exception:
            print("Account not found.")
