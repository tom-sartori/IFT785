import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox

from Account import Account
from Ledger import Ledger
from fake_crypto import generate_keys
from to_generate.OpenBlock import OpenBlock


def create_account(name):
    print("Creating account...")
    if is_account_already_exist(name):
        messagebox.showinfo("Error", "Account Already Exist")
        raise Exception("Account Already Exist")
    else:
        account = Account(*generate_keys(name))
        Ledger().add_account(account)
        update_ledger_display()


def create_block(public_key, bloc_type, balance):
    print("Building block...")
    account = Ledger().get_account(public_key)
    print(account.public_key.key)
    if account is None:
        messagebox.showinfo("Error", "Account Not Found")
        raise Exception("Account Not Found")
    else:
        # Test bloc creation
        bloc = OpenBlock(
            previous_block=account.head,
            unit='nano_coin',
            balance=balance,
            account=account.public_key.key
        )

        account.add_block(bloc)
        update_ledger_display()


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
        _, public_key, bloc_type, data = command.split()
        create_block(public_key, bloc_type, data)
        messagebox.showinfo("Success", f"Bloc successfully created with data: {data}")
    else:
        messagebox.showerror("Error", "Invalid command command.")
    command_entry.delete("1.0", tk.END)


# Configuration de l'interface graphique
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

# Configuration de l'affichage du Ledger
ledger_view = ttk.Treeview(root, columns=('Name', 'PublicKey', 'Blocks'), show='headings')
ledger_view.heading('Name', text='Account owner')
ledger_view.heading('PublicKey', text='Public key')
ledger_view.heading('Blocks', text='Number of blocks')
ledger_view.pack()

root.mainloop()
