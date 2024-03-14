from V2.Block import Block


class ReceiveBlock(Block):

    def __init__(self, source: str, previous_block: 'Block', data: dict = None):
        super().__init__(previous_block, data)

        self.add_data('source', source)
        # TODO: Update the balance of the account, within the Ledger.
