from V2.Block import Block


class OpenBlock(Block):

    def __init__(self):
        super().__init__()

        self.previous_hash = None
        self.add_data('balance', 0.0)
