from Block import Block
from Ledger import Ledger
from SendBlock import SendBlock
from fake_crypto import PublicKey

class ReceiveBlock(Block):
     def __init__(self, previous_block: Block,ledger:Ledger,pbkey:PublicKey):
          super().__init__(previous_block)

          self.ledger=ledger
          self.previous_block=previous_block
          self.pbkey=pbkey

          for pkey,acc in self.ledger._accounts.items():
               if pkey != self.pbkey:
                    for blc in acc._chain._block_list:
                         if isinstance(blc,SendBlock) and blc.data.get('destination')== self.pbkey:
                            self.add_data('block_type'  ,type(self).__name__)
                            self.add_data('balance',(self.previous_block.data.get('balance')+blc.data.get('amount_to_send')))
                            self.add_data('unit',blc.data.get('unit'))
                            self.add_data('amount_receive',blc.data.get('amount_to_send'))
                    
                              
