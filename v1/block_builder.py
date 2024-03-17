from generic_block import GenericBlock
from send_block import SendBlock
from account  import Account
# from receive_block import ReceiveBlock


class BlockBuilder():
    def __init__(self):
        self.data = dict()
        
    def set_param(self, key, value):
        self.data[key] = value
        return self  
    
    def set_previous_hash(self, hash):
        self.previous_hash = hash
        return self

    def build(self):
        # return globals.get(data["type"])(self.data)
        return GenericBlock(self.data)
    
class SendBlockBuilder(BlockBuilder):
    def __init__(self):
        super().__init__()
        self.previous_hash = None
        
    def set_balance(self, balance):
        self.data["balance"] = balance
    
    def destination(self, destination:Account):
        self.data["destination"] = destination
    
    def build(self):
        # return globals.get(data["type"])(self.data)
        return SendBlock(self.data)
    