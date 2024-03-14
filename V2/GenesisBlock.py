from V2.Block import Block
from V2.CONSTANT import GENESIS_BALANCE


class GenesisBlock(Block):

    def __init__(self):
        super().__init__()

        self.previous_hash = None
        self.add_data("balance", GENESIS_BALANCE)
