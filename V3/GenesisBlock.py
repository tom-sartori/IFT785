from V3.Block import Block


class GenesisBlock(Block):

    def __init__(self):
        super().__init__(None)

        self._header.previous_hash = None
