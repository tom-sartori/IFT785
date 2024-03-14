from V2.Block import Block
from V2.fake_crypto import PublicKey


class OpenBlock(Block):

    def __init__(self, public_key: PublicKey, previous_block: 'Block' = None, data: dict = None):
        super().__init__(previous_block, data)

        self.previous_hash = None
        # self.add_data('balance', 0.0)
        self.add_data('account', public_key)
        self.add_data('source', None)  # Should store the hash of the send block that created this account.
        self.add_data('representative', public_key)
        # TODO: Should update the new balance in the ledger.
