from command_manager.Command import Command


class HelpCommand(Command):
    """
    Some commands can implement simple operations on their own.
    """

    def __init__(self):
        result = '******** All commands available ******** \n \n'
        result += f"help: Display this help information  < {', '.join([])} \n"
        result += f"create_account: Add a new user  < {', '.join(['[user_name]'])}\n"
        result += (f"add_block: Add a new block on ledger  <  "
                   f"\n For OpenBlock : {', '.join([ '[block_type], [owner_public_key], [unit], [balance], [minimal_balance]'])}"
                   f"\n For SendBlock : {', '.join(['[block_type], [owner_public_key], [receiver_public_key], [amount_to_send]'])}"
                   f"\n For ReceiveBlock : {', '.join(['[block_type], [receiver_public_key], [sender_public_key]'])} \n")
        result += f"show_account: Display the account of current user  < {', '.join(['[public_key]'])}\n"
        result += f"show_accounts: Display all accounts of ledger < {', '.join([])}\n"
        result += f"show_blocks: Display all blocks of ledger  < {', '.join([])}\n"
        result += f"show_ledger: Display the ledger  < {', '.join([])}\n"

        self.commands = result

    def execute(self) -> None:
        result = 'Nano BlockChain Shell Commands, version 2.1: \n'
        result += 'These shell commands are defined internally.  Type `help` to see this list.: \n\n'
        print(self.commands)
        with open("commands_help.txt", "w") as file:
            file.write(self.commands)
        print("Help information has been written to commands_help.txt")
