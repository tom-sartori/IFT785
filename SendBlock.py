from Block import Block
from Account import Account


class SendBlock(Block):
    def __init__(self, previous_block: Block,acc:Account,balance:int or float,unit:str):
        super().__init__(previous_block)
        
        self.acc =acc
        self.balance = balance
        self.unit = unit
        self.previous_block = previous_block

        if self.previous_block.data.get('balance')>self.balance and self.previous_block.data.get('unit')== self.unit:

            self.previous_block.data.__setitem__('balance',(self.previous_block.data.get('balance')-self.balance))

            self.add_data('destination' ,str(acc.public_key))
            self.add_data('block_type'  ,'send')
        else:
            raise Exception('Error: Balance Faible ')
        
        
        


            
     
    

