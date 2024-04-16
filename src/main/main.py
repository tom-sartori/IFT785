from dsl.BlockTypeRegister import BlockTypeRegister
from dsl.Dsl import Dsl
from ledger.Ledger import Ledger
from ledger.account.Account import Account
from Interpreter import Interpreter
from command_manager.Invoker import Invoker
from command_manager.Receiver import Receiver
from command_manager.CreateAccountCommand import CreateAccountCommand
from command_manager.AddBlockCommand import AddBlockCommand
from command_manager.HelpCommand import HelpCommand
from command_manager.ShowAccountCommand import ShowAccountCommand
from command_manager.ShowAllAccountsCommand import ShowAllAccountsCommand
from command_manager.ShowBlocksCommand import ShowBlocksCommand
from command_manager.ShowLedgerCommand import ShowLedgerCommand
from utils.fake_crypto import generate_keys


if __name__ == '__main__':
    # Load the DSL and create the block types.
    # dsl: Dsl = Dsl(dsl_file_name='resources/dsl.json')
    # BlockTypeRegister().add_block_types(dsl.blocks)
    # print(BlockTypeRegister())
    #
    # # Create two accounts.
    # genesis_account: Account = Account(*generate_keys('Genesis'))
    # Ledger().add_account(genesis_account)
    # second_account: Account = Account(*generate_keys('Second'))
    # Ledger().add_account(second_account)
    #
    # # Open Nanocoin for Genesis.
    # genesis_open_nanocoin = BlockTypeRegister()['OpenNanocoin'](genesis_account.head)
    # genesis_account.add_block(genesis_open_nanocoin)
    #
    # # Open Nanocoin for Second.
    # second_account.add_block(BlockTypeRegister()['OpenNanocoin'](second_account.head))
    #
    # # Send 50 Nanocoins from Genesis to Second.
    # send_block = BlockTypeRegister()['Send'](
    #     previous_block=genesis_account.head,
    #     receiver=second_account.public_key.key,
    #     amount=40,
    #     open_hash=genesis_open_nanocoin.hash)
    # genesis_account.add_block(send_block)
    #
    # # Receive Nanocoins from Genesis to Second.
    # receive_block = BlockTypeRegister()['Receive'](previous_block=second_account.head, send_hash=send_block.hash)
    # second_account.add_block(receive_block)
    #
    # print(Ledger())
    #
    # print(genesis_account.balances)
    # print(second_account.balances)
    # command_manager = Interpreter()
    # command_manager.run()

    """
        The client code can parameterize an invoker with any commands.
        """

    interpreter = Interpreter()
    receiver = Receiver()
    invoker = Invoker()


    while True:
        command_input = input("Enter command: ")
        parts = command_input.split()
        command = parts[0]
        args = parts[1:]

        if command == "create_account":
            user_name = ' '.join(args)
            create_account_command = CreateAccountCommand(user_name)
            invoker.register_command(command_input, create_account_command)
            invoker.execute_command(command_input)
        elif command == "add_block":
            add_block_command = AddBlockCommand(receiver, args)
            invoker.register_command(command_input, add_block_command)
            invoker.execute_command(command_input)
        elif command == "show_all_blocks":
            show_blocks_command = ShowBlocksCommand()
            invoker.register_command(command_input, show_blocks_command)
            invoker.execute_command(command_input)
        elif command == "show_ledger":
            show_ledger_command = ShowLedgerCommand()
            invoker.register_command(command_input, show_ledger_command)
            invoker.execute_command(command_input)
        elif command == "show_account":
            public_key = ' '.join(args)
            show_account_command = ShowAccountCommand(public_key)
            invoker.register_command(command_input, show_account_command)
            invoker.execute_command(command_input)
        elif command == "show_all_accounts":
            show_all_accounts_command = ShowAllAccountsCommand()
            invoker.register_command(command_input, show_all_accounts_command)
            invoker.execute_command(command_input)
        elif command == "help":
            help_command = HelpCommand()
            invoker.register_command(command_input, help_command)
            invoker.execute_command(command_input)
        elif command_input == "exit":
            break
        else:
            print("Unknown command.")
            continue

        invoker.register_command(command_input, command)
        invoker.execute_command(command_input)

    """
            uncomment the following lines and run main.py to do a quick test or run the main in command_manager mode.
    """

    # command_manager.create_account("Alice")
    # command_manager.create_account("Bob")
    #
    # # Create Alice Account
    # command_manager.create_open_block(
    #     "4A20360DF0FDC9979B30BCB50318521E4DC9C05F",
    #     "OpenNanocoin",
    #     "Nanocoin",
    #     200,
    #     0
    # )
    #
    # # Create Bob Account
    # command_manager.create_open_block(
    #     "9AF3883DC6725FBF664400A8FA2C2F7FD6998629",
    #     "OpenNanocoin",
    #     "Nanocoin",
    #     200,
    #     0
    # )
    #
    # # send 25 from Alice to Bob
    # command_manager.create_send_block(
    #     "4A20360DF0FDC9979B30BCB50318521E4DC9C05F",
    #     "9AF3883DC6725FBF664400A8FA2C2F7FD6998629",
    #     25
    # )
    #
    # # Receive 25 Nanocoins from Alice.
    # command_manager.create_receive_block(
    #     "9AF3883DC6725FBF664400A8FA2C2F7FD6998629",
    #     "4A20360DF0FDC9979B30BCB50318521E4DC9C05F"
    # )
