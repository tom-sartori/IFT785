from Block import Block


class GenesisBlock(Block):

    def __init__(self):
        super().__init__(previous_block=None)
