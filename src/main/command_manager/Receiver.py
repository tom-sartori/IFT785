import json

from Interpreter import Interpreter

from dsl.BlockTypeRegister import BlockTypeRegister
from dsl.Dsl import Dsl
from ledger.Ledger import Ledger

class Receiver:
    """
    The Receiver classes contain some important business logic. They know how to
    perform all kinds of operations, associated with carrying out a request. In
    fact, any class may serve as a Receiver.
    """
    def __init__(self):
        self.file_path = 'resources/dsl.json'
        with open(self.file_path, 'r') as file:
            data = json.load(file)

        self.block_types = list(data['blocks'].keys())

    def add_particular_block(self, args: list) -> None:
        block_type = args[0]
        if block_type in self.block_types:
            if block_type.lower() == 'opennanocoin':
                _, owner_public_key, block_type, unit, balance, minimal_balance, *_ = args
                self.__create_open_block(owner_public_key, block_type, unit, balance, minimal_balance)
            elif block_type.lower() == 'send':
                _, owner_public_key, receiver_public_key, amount_to_send, *_ = args
                self.__create_send_block(owner_public_key, receiver_public_key, amount_to_send)
            elif block_type.lower() == 'receive':
                _, owner_public_key, sender_public_key, *_ = args
                self.__create_receive_block(owner_public_key, sender_public_key)
            else:
                print(f"\nReceiver: Unknown block type: {block_type}")

    def __create_open_block(self, owner_public_key, block_type, unit, balance, minimal_balance):
        print("Building Open block...")
        account = Ledger().get_account(str(owner_public_key))
        if account is None:
            raise Exception("Account Not Found")
        else:
            self.__update_json_dsl_file(str(block_type), str(unit), int(balance), int(minimal_balance))
            dsl: Dsl = Dsl(dsl_file_name='resources/dsl.json')
            BlockTypeRegister().add_block_types(dsl.blocks)
            bloc = BlockTypeRegister()['OpenNanocoin'](account.head)
            account.add_block(bloc)

    def __create_send_block(self, owner_public_key, receiver_public_key, amount_to_send):
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
            else:
                raise Exception("Receiver Account Not Found")

    def __create_receive_block(self, owner_public_key, sender_public_key):
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
            else:
                raise Exception("Sender Account Not Found")

    def __update_json_dsl_file(self, block_type, unit, balance, minimal_balance):
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

    def __is_account_already_exist(self, name):
        accounts = Ledger()._accounts.values()
        for account in accounts:
            if account.public_key.owner == name:
                return True
            return False
