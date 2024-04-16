from command_manager.Command import Command


class HelpCommand(Command):
    """
    Some commands can implement simple operations on their own.
    """

    def __init__(self):
        result = ''
        result += f"help: Display this help information\n  Args: {', '.join([])}"
        result += f"add_block: Add a new block on ledger\n  Args: {', '.join(['owner_public_key', '[receiver_public_key]', '[amount_to_send]',  'block_type', 'unit', 'balance', 'minimal_balance'])}"
        result += f"create_account: Add a new user\n  Args: {', '.join(['user_name'])}"
        result += f"show_account: Display the account of current user\n  Args: {', '.join(['public_key'])}"
        result += f"show_all_accounts: Display all accounts of ledger\n  Args: {', '.join([])}"
        result += f"show_all_blocks: Display all blocks of ledger\n  Args: {', '.join([])}"
        result += f"show_ledger: Display the ledger\n  Args: {', '.join([])}"

        self.commands = result

    def execute(self) -> None:
        result = 'Nano BlockChain Shell Commands, version 2.1: \n'
        result += 'These shell commands are defined internally.  Type `help` to see this list.: \n\n'
        print(self.commands)
