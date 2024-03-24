from functools import partial
import inspect

from Account import Account
from Chain import Chain
from Block import Block

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


#Fonction pour l'interpréteur
def getNumberOfArgument(fonction) -> int:
    return len(inspect.getfullargspec(fonction).args)

def isEqual(arg1, arg2) -> bool:
    return arg1 == arg2

def greaterThan(arg1, arg2) -> bool:
    return arg1 > arg2

def lessThan(arg1, arg2) -> bool:
    return not greaterThan(arg1, arg2)
