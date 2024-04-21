from src.main.ledger.block.Block import Block


class OpenBlock(Block):

    def __init__(self, previous_block: Block, unit: str, balance: int or float, account: str = None):
        # TODO: Class Unit.
        # account = public_key.key
        # If account is None, then add the balance to all accounts that use this open block.
        # If account is set, then add the balance only to the account that uses this open block.
        super().__init__(previous_block)

        (self.add_data('unit', unit)
         .add_data('balance', balance)
         .add_data('account', account))
