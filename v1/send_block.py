from generic_block import GenericBlock

class SendBlock(GenericBlock):
    def __init__(self, data, previous_hash):
        super().__init__(data, previous_hash)
        self._data["type"] = "Generic Block"
