from command_manager.AddBlockCommand import AddBlockCommand
from command_manager.CreateAccountCommand import CreateAccountCommand
from command_manager.HelpCommand import HelpCommand
from command_manager.ShowAccountCommand import ShowAccountCommand
from command_manager.ShowAllAccountsCommand import ShowAllAccountsCommand
from command_manager.ShowBlocksCommand import ShowBlocksCommand
from command_manager.ShowLedgerCommand import ShowLedgerCommand


class CommandFactory:
    def __init__(self, invoker, receiver):
        self.invoker = invoker
        self.receiver = receiver

    def get_command(self, command_input):
        parts = command_input.split()
        command = parts[0].lower()
        args = parts[1:]

        command_map = {
            "create_account": CreateAccountCommand(' '.join(args)),
            "add_block": AddBlockCommand(self.receiver, args),
            "show_blocks": ShowBlocksCommand(),
            "show_ledger": ShowLedgerCommand(),
            "show_account": ShowAccountCommand(' '.join(args)),
            "show_accounts": ShowAllAccountsCommand(),
            "help": HelpCommand(),
        }

        return command_map.get(command)
