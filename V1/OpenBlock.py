from Block import Block


class OpenBlock(Block):

    def __init__(self, previous_block: 'Block' or None):
        super().__init__(previous_block)
