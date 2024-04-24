from main.command_manager.commands.Command import Command
from main.dsl.BlockTypeRegister import BlockTypeRegister
from main.ledger.Ledger import Ledger
from main.ledger.account.Account import Account
from main.ledger.block.Block import Block


class AddBlockCommand(Command):

    def __init__(self, block_type: str, previous_hash: str, args: []) -> None:
        self.block_type = block_type
        self.previous_hash = previous_hash
        self.args = args

    def execute(self) -> None:
        try:
            previous_block: Block = Ledger().get_block(self.previous_hash)
        except Exception:
            print(f"Previous block {self.previous_hash} not found. ")
            return

        try:
            account: Account = Ledger().get_account(previous_block.account_public_key)
        except Exception:
            print(f"Account {previous_block.account_public_key} not found. ")
            return

        try:
            BlockType = BlockTypeRegister()[self.block_type]
        except Exception:
            print(f"Block type {self.block_type} not found. ")
            return

        try:
            block = BlockType(previous_block, *self.args) if self.args else BlockType(previous_block)
        except Exception as e:
            print(f"Error creating block: {e}")
            return

        try:
            account.add_block(block)
        except Exception as e:
            print(f"Error adding block to account: {e}")
            return

        print(f"Block {self.block_type} added to account {account.public_key.key} with hash {block.hash}. ")
