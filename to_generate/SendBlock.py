from Block import Block
from Account import Account
from to_generate.ReceiveBlock import ReceiveBlock


class SendBlock(Block):

    def __init__(self, previous_block: Block, unit: str, amountSend: int or float, senderAccount: Account, receiverAccount: Account):
        
        super().__init__(previous_block)
        (self.add_data('unit', unit)
        .add_data('amountSend', amountSend)
        .add_data('senderAccount', senderAccount.public_key.key)
        .add_data('receiverAccount', receiverAccount.public_key.key))

        #self.unit = unit,
        #self.amountSend = amountSend,
        #self.senderAccount = senderAccount.public_key.key,
        #self.receiverAccount = receiverAccount.public_key.key

        self._addBlockToReceiver(senderAccount, receiverAccount)


    def _addBlockToReceiver(self, accountSource: Account, accountDestination: Account):
        blockToReceive = ReceiveBlock(
            previous_block= accountDestination.head,
            unit=self.get_data('unit'),
            amountSend=self.get_data('amountSend'),
            senderAccount=accountSource,
            receiverAccount=accountDestination
        )

        accountDestination.add_block(blockToReceive)
