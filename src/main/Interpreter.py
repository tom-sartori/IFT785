"""
        Creation of accounts and blocks from the graphical interface.

        account creation syntax: create_account <account_name>
        syntax for creating a block: create_block <owner_public_key> <receiver_public_key> <bloc_type> <unit> <balance> <minimal_balance>
        receiver_public_key is the public key of the receiver account, and it's optional.

        We must create an account before creating blocks
"""


import json
from dsl.BlockTypeRegister import BlockTypeRegister
from dsl.Dsl import Dsl
from ledger.Ledger import Ledger
from ledger.account.Account import Account
from utils.fake_crypto import generate_keys

class Interpreter(object):
    def __init__(self):
        print(" **** Interpreter Command ****")
        self.file_path = 'resources/dsl.json'

    def create_account(self, name):
        print("Creating account...")
        if self.is_account_already_exist(str(name)):
            raise Exception("Account Already Exist")
        else:
            account = Account(*generate_keys(str(name)))
            Ledger().add_account(account)
            self.print_display()

    def create_open_block(self, owner_public_key, block_type, unit, balance, minimal_balance):
        print("Building Open block...")
        account = Ledger().get_account(str(owner_public_key))
        if account is None:
            raise Exception("Account Not Found")
        else:
            self.update_json_dsl_file(str(block_type), str(unit), int(balance), int(minimal_balance))
            dsl: Dsl = Dsl(dsl_file_name='resources/dsl.json')
            BlockTypeRegister().add_block_types(dsl.blocks)
            bloc = BlockTypeRegister()['OpenNanocoin'](account.head)
            account.add_block(bloc)
            self.print_display()

    def create_send_block(self, owner_public_key, receiver_public_key, amount_to_send):
        print("Building Send block...")

        account = Ledger().get_account(str(owner_public_key))
        receiver_account = Ledger().get_account(str(receiver_public_key))

        if account is None:
            raise Exception("Account Not Found")
        else:
            if receiver_account is not None:
                account.add_block(
                    BlockTypeRegister()['Send'](
                        previous_block=account.head,
                        receiver=receiver_account.public_key.key,
                        amount=int(amount_to_send),
                        open_hash=account.head.hash)
                )
                self.print_display()
            else:
                raise Exception("Receiver Account Not Found")

    def create_receive_block(self, owner_public_key, sender_public_key):
        print("Building Receive block...")
        account = Ledger().get_account(owner_public_key)
        sender_account = Ledger().get_account(sender_public_key)
        if account is None:
            raise Exception("Account Not Found")
        else:
            if sender_account is not None:
                account.add_block(
                    BlockTypeRegister()['Receive'](
                        previous_block=account.head,
                        send_hash=sender_account.head.hash)
                )
                self.print_display()
            else:
                raise Exception("Sender Account Not Found")

    def update_json_dsl_file(self, block_type, unit, balance, minimal_balance):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        if 'blocks' in data and 'OpenNanocoin' in data['blocks']:
            # Rename 'OpenNanocoin' key to 'NewBlockType'
            data['blocks'][block_type] = data['blocks'].pop('OpenNanocoin')

            # Edit 'unit', 'balance' and 'minimal_balance' attributes
            data_block = data['blocks'][block_type]
            data_block['unit'] = unit
            data_block['balance'] = balance
            data_block['minimal_balance'] = minimal_balance

        # Write changes back to JSON file
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def print_display(self):
        print(Ledger())

    def is_account_already_exist(self, name):
        accounts = Ledger()._accounts.values()
        for account in accounts:
            if account.public_key.owner == name:
                return True
            return False
