"""
        Creation of accounts and blocks from the graphical interface.

        account creation syntax: create_account <account_name>
        syntax for creating a block: create_block <owner_public_key> <receiver_public_key> <bloc_type> <unit> <balance> <minimal_balance>
        receiver_public_key is the public key of the receiver account, and it's optional.

        We must create an account before creating blocks
"""

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox

from Account import Account
from BlockTypeRegister import BlockTypeRegister
from Dsl import Dsl
from Ledger import Ledger
from fake_crypto import generate_keys
import json


def create_account(name):
    print("Creating account...")
    if is_account_already_exist(name):
        messagebox.showinfo("Error", "Account Already Exist")
        raise Exception("Account Already Exist")
    else:
        account = Account(*generate_keys(name))
        Ledger().add_account(account)
        update_ledger_display()


def create_block(owner_public_key, receiver_public_key, block_type, unit, balance, minimal_balance):
    file_path = 'dsl/dsl.json'

    print("Building block...")
    account = Ledger().get_account(owner_public_key)
    receiver_account = Ledger().get_account(receiver_public_key)
    print(account.public_key.key)
    if account is None:
        messagebox.showinfo("Error", "Account Not Found")
        raise Exception("Account Not Found")
    else:
        update_json_dsl_file(file_path, block_type, unit, balance, minimal_balance)
        dsl: Dsl = Dsl(dsl_file_name='dsl/dsl.json')
        BlockTypeRegister().add_block_types(dsl.blocks)
        print(BlockTypeRegister())

        bloc = BlockTypeRegister()['OpenNanocoin'](account.head)
        account.add_block(bloc)
        if receiver_account is not None:
            account.add_block(
                BlockTypeRegister()['Send'](account.head, receiver_account.public_key.key, 25, bloc.hash)
            )

        update_ledger_display()


def update_json_dsl_file(file_path, block_type, unit, balance, minimal_balance):
    with open(file_path, 'r') as file:
        data = json.load(file)
    # Modify attributes according to provided variables
    if 'blocks' in data and 'OpenNanocoin' in data['blocks']:
        # Rename 'OpenNanocoin' key to 'NewBlockType'
        data['blocks'][block_type] = data['blocks'].pop('OpenNanocoin')

        # Edit 'unit', 'balance' and 'minimal_balance' attributes
        if 'data' in data['blocks'][block_type]:
            data_block = data['blocks'][block_type]['data']
            data_block['unit'] = unit
            data_block['balance'] = int(balance)
            data_block['minimal_balance'] = int(minimal_balance)

    # Write changes back to JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def update_ledger_display():
    accounts = Ledger()._accounts.values()
    # Clear existing entries
    for item in ledger_view.get_children():
        ledger_view.delete(item)
    print(accounts)

    # Add ledger accounts to Treeview
    for account in accounts:
        print(account.public_key.key)
        ledger_view.insert('', tk.END, values=(account.public_key.owner, account.public_key.key, len(account._chain)))

    print(Ledger())


def is_account_already_exist(name):
    accounts = Ledger()._accounts.values()
    print(accounts)
    for account in accounts:
        if account.public_key.owner == name:
            return True
        return False


def process_command():
    command = command_entry.get("1.0", tk.END).strip()
    if command.startswith("create_account"):
        _, name = command.split()
        create_account(name)
        messagebox.showinfo("Success", f"Account '{name}' successfully created!")
    elif command.startswith("create_block"):
        _, public_key, receiver_public_key, bloc_type, unit, balance, minimal_balance = command.split()
        create_block(public_key, receiver_public_key, bloc_type, unit, balance, minimal_balance)
        messagebox.showinfo("Success", "Bloc successfully created")
    else:
        messagebox.showerror("Error", "Invalid command command.")
    command_entry.delete("1.0", tk.END)


# Configuring the GUI
root = tk.Tk()
root.title("Nano Blockchain Command Interface")

command_label = tk.Label(root, text="Enter your command:")
command_label.pack()

command_entry = scrolledtext.ScrolledText(root, height=4)
command_entry.pack()

submit_button = tk.Button(root, text="Execute", command=process_command)
submit_button.pack()

ledger_label = tk.Label(root, text="Ledger (Accounts):")
ledger_label.pack()

# Configuring the Ledger display
ledger_view = ttk.Treeview(root, columns=('Name', 'PublicKey', 'Blocks'), show='headings')
ledger_view.heading('Name', text='Account owner')
ledger_view.heading('PublicKey', text='Public key')
ledger_view.heading('Blocks', text='Number of blocks')
ledger_view.pack()

root.mainloop()
