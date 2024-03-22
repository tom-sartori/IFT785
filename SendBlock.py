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

            
            self.add_data('destination' ,acc.public_key.key)
            self.add_data('block_type'  ,type(self).__name__)
            self.add_data('last_balance',self.previous_block.data.get('balance'))
            self.add_data('balance',(self.previous_block.data.get('balance')-self.balance))
            self.add_data('unit',self.unit)
            self.add_data('amount_to_send',self.balance)
        else:
            raise Exception('Error: Balance Faible ou Devise inexistant')
        
        
        


            
     
    

