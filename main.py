from Account import Account
from Ledger import Ledger
from fake_crypto import generate_keys
from to_generate.OpenBlock import OpenBlock
from to_generate.EmptyBlock import EmptyBlock
from Block_test import Block_test

from fonction import *


if __name__ == '__main__':
    '''
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
    
   


    #Exemple d'utilisation de fonction
    newBlock = EmptyBlock(genesis_account.head)
    
    blockExistInChain(genesis_account, open_block_genesis)
    blockExistInChain(genesis_account, newBlock)

    enoughtCreditInAccount(genesis_account, 'nano_coin', 5)
    enoughtCreditInAccount(genesis_account, 'nano_coin', 2000)

    print(isEqual(2, 2))
    print(isEqual(2, 3))

    print(greaterThan(3, 2))
    print(greaterThan(1, 2))

    print(lessThan(1, 2))
    print(lessThan(3, 2))

    print(getNumberOfArgument(enoughtCreditInAccount))
    print(getNumberOfArgument(isEqual))

    print(addCreditToAccount(genesis_account, newBlock ,'nano_coin', 5))
    print(removeCreditFromAccount(genesis_account, newBlock, 'nano_coin', 5))

    print(addCurrency(newBlock, 'nano2', 20000))
    '''

    #Exemple du nouveau bloc
    ledger1: Ledger = Ledger()

    #Exemple de création de compte
    account1: Account = Account(*generate_keys('account1'))
    ledger1.add_account(account1)

    blockTest = Block_test(previous_block=account1.head)
    blockTest.addAction(addCurrency, ['unit', 'startingNumber'])
    blockTest.addDataForFunction('unit', '\'nano\'').addDataForFunction('startingNumber', 1000)

    blockTest.executeAllAction()


    account1.add_block(blockTest)

    print(account1)
