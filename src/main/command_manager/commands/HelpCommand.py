from command_manager.commands.Command import Command


class HelpCommand(Command):
    """
    Some commands can implement simple operations on their own.
    """

    def __init__(self):
        result = '******** All available commands ******** \n \n'
        result += f"help: Show available commands  < {', '.join([])} \n"
        result += f"create_account: Add a new user  < {', '.join(['[user_name]'])}\n"
        result += f"add_block: Add a new block to an account. See show_blocks for block's params  < [block_type] [params] \n"
        result += f"show_account: Show account details  < {', '.join(['[public_key]'])}\n"
        result += f"show_accounts: Show all accounts on ledger < {', '.join([])}\n"
        result += f"show_blocks: Show available block types from the dsl  < {', '.join([])}\n"
        result += f"show_ledger: Show the ledger  < {', '.join([])}\n"

        self.commands = result

    def execute(self) -> None:
        result = 'Nano BlockChain Shell Commands, version 2.1: \n'
        result += 'These shell commands are defined internally.  Type `help` to see this list.: \n\n'
        print(self.commands)
        with open("commands_help.txt", "w") as file:
            file.write(self.commands)
        print("Help information has been written to commands_help.txt")
