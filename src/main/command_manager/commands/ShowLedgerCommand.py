from command_manager.commands.Command import Command
from ledger.Ledger import Ledger


class ShowLedgerCommand(Command):
    """
    Some commands can implement simple operations on their own.
    """

    def execute(self) -> None:
        print(Ledger())
