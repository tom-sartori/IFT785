from Block import Block
from Account import Account


class ReceiveBlock(Block):

    def __init__(self, previous_block: Block, unit: str, amountSend: int or float, senderAccount: Account, receiverAccount: Account):
        
        super().__init__(previous_block)
        (self.add_data('unit', unit)
        .add_data('amountSend', amountSend)
        .add_data('senderAccount', senderAccount.public_key.key)
        .add_data('receiverAccount', receiverAccount.public_key.key))
        
        #(self.add_data('unit', unit)
        # .add_data('amountSend', amountSend)
        # .add_data('senderAccount', senderAccount.public_key.key)
        # .add_data('receiverAccount', receiverAccount.public_key.key))
    
