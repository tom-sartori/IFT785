from Block import Block



class EmptyBlock(Block):

    def __init__(self, previous_block: Block):
        super().__init__(previous_block)
