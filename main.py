from Account import Account
from Ledger import Ledger
from fake_crypto import generate_keys
from OpenBlock import OpenBlock
from SendBlock import SendBlock


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

    c: Account = Account(*generate_keys('Test'))


    genesis_account.add_block(open_block_genesis)


    send_test = SendBlock(open_block_genesis,
                          c,
                          100,
                          'nano_coin'
                          )
    

    genesis_account.add_block(send_test)
    
    print(genesis_account)
    
    #print(ledger)
 

   
        
