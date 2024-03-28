from functools import partial
import inspect

#from Account import Account
#from Chain import Chain
#from Block import Block
from Block_test import Block_test

'''
def add_method(objet: object, fonction):
    setattr(objet, fonction.__name__, partial(fonction, objet))




def blockExistInChain(account: Account, block: Block) -> bool:

    block_list : list[Block] = account.getChain().getBlockList()
    
    for block_ in block_list:
        if (block_.getBlockType == block.getBlockType):
            print("This block exist in this chain")
            return True

    print("This block don't exist in this chain")
    return False


def enoughtCreditInAccount(account: Account, creditType: str, numberCreditNeeded: int or float) -> bool:
    if (account.getChain().get_balance(creditType) >= numberCreditNeeded):
        print("Enought credit in this account")
        return True
    
    print("Not enought credit in this account")
    return False


def addCreditToAccount(account: Account, block: Block, unit: str, numberCreditToAdd: int or float) -> Block:
    assert numberCreditToAdd > 0
    return block.add_data('unit', unit).add_data('balance', account.getChain().get_balance(unit) + numberCreditToAdd)


def removeCreditFromAccount(account: Account, block: Block, unit: str, numberCreditToRemove: int or float) -> Block:
    assert numberCreditToRemove > 0
    return block.add_data('unit', unit).add_data('balance', account.getChain().get_balance(unit) - numberCreditToRemove)
'''

def addCurrency(bloc: Block_test, unit: str, startingNumberOfCredit: int or float):
    bloc.balance[unit] = startingNumberOfCredit






#Fonction pour l'interpréteur
def getNumberOfArgument(fonction) -> int:
    return len(inspect.getfullargspec(fonction).args)

def isEqual(arg1, arg2) -> bool:
    return arg1 == arg2

def greaterThan(arg1, arg2) -> bool:
    return arg1 > arg2

def lessThan(arg1, arg2) -> bool:
    return not greaterThan(arg1, arg2)
