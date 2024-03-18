from V3.Block import Block
from V3.fake_crypto import PublicKey


class GenesisBlock(Block):

    def __init__(self, public_key: PublicKey):
        super().__init__(None)

        self._header.previous_hash = None
        self.account: str = public_key.key
