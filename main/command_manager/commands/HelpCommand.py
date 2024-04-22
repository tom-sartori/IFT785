from main.command_manager.commands.Command import Command


class HelpCommand(Command):
    """
    Some commands can implement simple operations on their own.
    """

    def __str__(self) -> str:
        result = '******** All available commands ******** \n \n'
        result += f"help: Show available commands  < {', '.join([])} \n"
        result += f"create_account: Add a new user  < {', '.join(['[user_name]'])}\n"
        result += f"add_block: Add a new block to an account. See show_blocks for block's params  < [block_type] [params...] \n"
        result += f"\t Example: add_block OpenNanocoin 840A39B855362D7978BFA94F1193901D7AE37DEC\n"
        result += f"show_account: Show account details  < {', '.join(['[public_key]'])}\n"
        result += f"show_accounts: Show all accounts on ledger < {', '.join([])}\n"
        result += f"show_blocks: Show available block types from the dsl  < {', '.join([])}\n"
        result += f"show_ledger: Show the ledger  < {', '.join([])}\n"

        return result

    def execute(self) -> None:
        print(self)
        with open("commands_help.txt", "w") as file:
            file.write(self.__str__())
        print("Help information has been written to commands_help.txt\n")
