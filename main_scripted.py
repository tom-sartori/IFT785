from main.command_manager.Invoker import Invoker
from main.ledger.Ledger import Ledger
from main.ledger.account.Account import Account

if __name__ == "__main__":
    Invoker('help').execute()
    Invoker('create_account Jean').execute()
    # Get first element of Ledger().accounts.values() to get the first account created.
    jean_account: Account = list(Ledger().accounts.values())[0]

    # OpenNanocoin(previous_block)
    command = f'add_block OpenNanocoin {jean_account.head.hash}'
    print(f'Command: {command}')
    Invoker(command).execute()

    # Send(previous_block, receiver, amount, open_hash)
    command = f'add_block Send {jean_account.head.hash} {jean_account.public_key.key} 40 {jean_account.head.hash}'
    print(f'Command: {command}')
    Invoker(command).execute()

    # ShowAccount(public_key)
    command = f'show_account {jean_account.public_key.key}'
    print(f'Command: {command}')
    Invoker(command).execute()

    while True:
        command_input: str = input("\nEnter command: ")

        if command_input == "exit":
            print("Bye...")
            break

        Invoker(command_input).execute()
