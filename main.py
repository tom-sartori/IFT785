from Account import Account
from Ledger import Ledger
from fake_crypto import generate_keys
from to_generate.OpenBlock import OpenBlock
from to_generate.SendBlock import SendBlock

if __name__ == '__main__':
    ledger: Ledger = Ledger()

    #Exemple de création de compte
    genesis_account: Account = Account(*generate_keys('Genesis'))
    ledger.add_account(genesis_account)

    open_block_genesis = OpenBlock(
        previous_block=genesis_account.head,
        unit='nano_coin',
        balance=1000,
        account=genesis_account.public_key.key
    )

    genesis_account.add_block(open_block_genesis)

    print(ledger)





    #Exemple d'echange
    Alice: Account = Account(*generate_keys('Genesis_Alice'))
    ledger.add_account(Alice)

    open_block_genesis = OpenBlock(
        previous_block=Alice.head,
        unit='nano_coin',
        balance=1000,
        account=Alice.public_key.key
    )

    Alice.add_block(open_block_genesis)


    Bob: Account = Account(*generate_keys('Genesis_Bob'))
    ledger.add_account(Bob)

    open_block_genesis = OpenBlock(
        previous_block=Bob.head,
        unit='nano_coin',
        balance=1000,
        account=Bob.public_key.key
    )

    Bob.add_block(open_block_genesis)

    send_block_Alice_Bob = SendBlock(
        previous_block=Alice.head,
        unit='nano_coin',
        amountSend=5,
        senderAccount=Alice,
        receiverAccount=Bob

    )

    Alice.add_block(send_block_Alice_Bob)

    print(ledger)
