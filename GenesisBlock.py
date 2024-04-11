from Block import Block
from fake_crypto import PublicKey


class GenesisBlock(Block):

    def __init__(self, public_key: PublicKey):
        super().__init__(None)

        self._header.previous_hash = None
        self.add_data('account', public_key.key)
