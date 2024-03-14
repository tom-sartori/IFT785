from V2.Account import Account
from V2.Block import Block


class SendBlock(Block):

    # Must have an open block before it.

    def __init__(self, previous_block: 'Block', balance: float, destination: Account, amount: float, data: dict = None):
        super().__init__(previous_block, data)

        if balance < amount:
            raise Exception("Insufficient funds. ")

        self.add_data('destination', destination)
        self.add_data('balance', balance - amount)
