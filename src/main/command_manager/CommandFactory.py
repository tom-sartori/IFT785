from command_manager.commands.AddBlockCommand import AddBlockCommand
from command_manager.commands.Command import Command
from command_manager.commands.CreateAccountCommand import CreateAccountCommand
from command_manager.commands.HelpCommand import HelpCommand
from command_manager.commands.ShowAccountCommand import ShowAccountCommand
from command_manager.commands.ShowAllAccountsCommand import ShowAllAccountsCommand
from command_manager.commands.ShowBlocksCommand import ShowBlocksCommand
from command_manager.commands.ShowLedgerCommand import ShowLedgerCommand
from utils.SingletonMeta import SingletonMeta


class CommandFactory(metaclass=SingletonMeta):

    def __getitem__(self, command_input: str) -> Command or None:
        parts = command_input.split()
        command = parts[0].lower()
        args = parts[1:]

        if command == 'create_account':
            return CreateAccountCommand(' '.join(args))
        elif command == 'show_blocks':
            return ShowBlocksCommand()
        elif command == "add_block":
            return AddBlockCommand(block_type=args[0], previous_hash=args[1], args=args[2:])
        elif command == 'show_ledger':
            return ShowLedgerCommand()
        elif command == 'show_account':
            return ShowAccountCommand(' '.join(args))
        elif command == 'show_accounts':
            return ShowAllAccountsCommand()
        elif command == 'help':
            return HelpCommand()
        else:
            return None
