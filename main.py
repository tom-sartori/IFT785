from Account import Account
from Ledger import Ledger
from fake_crypto import generate_keys,PublicKey
from OpenBlock import OpenBlock
from SendBlock import SendBlock
from ReceiveBlock import ReceiveBlock


if __name__ == '__main__':
    ledger: Ledger = Ledger()

    genesis_account: Account = Account(*generate_keys('Genesis'))
    ledger.add_account(genesis_account)

    open_block_genesis = OpenBlock(
        previous_block=genesis_account.head,
        unit='nano_coin',
        balance=1000,
        account=genesis_account.public_key.key
    )

    genesis_account.add_block(open_block_genesis)

    c: Account = Account(*generate_keys('Test'))
    ledger.add_account(c)

    open_c = OpenBlock(
        previous_block=c.head,
        unit='nano-coin',
        balance=1000,
        account=c.public_key.key
    )

    c.add_block(open_c)


    send_test = SendBlock(previous_block=open_block_genesis,
                          acc=c,
                          balance=100,
                          unit='nano-coin'
                          )
    genesis_account.add_block(send_test)


    receive_test = ReceiveBlock(previous_block=open_c,
                                ledger=ledger,
                                pbkey=c.public_key.key)
    
    c.add_block(receive_test)


    

    print(ledger)


    '''
     



    
    
       

    

   
    
    print(genesis_account)
    

    
 
'''
   
        
