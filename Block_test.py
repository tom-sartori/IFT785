import json
from abc import ABC
from textwrap import indent


from Header import Header
from fake_crypto import sha, new_deterministic_hash, Signature, PublicKey, sign, PrivateKey
#from fonction import *

class Block_test(ABC):

    @property
    def hash(self):
        return sha(self._header)


    @property
    def is_signed(self):
        return self._signature is not None


    def __init__(self, previous_block: 'Block_test', dataForFunction: dict = dict()):
        if previous_block is None:
            previous_hash: str = new_deterministic_hash()
            self.balance = dict()
        elif isinstance(previous_block, Block_test):
            previous_hash: str = previous_block.hash
            self.balance = previous_block.balance
        else:
            raise Exception("previous_block must be Block or None. ")

        self._header = Header(previous_hash=previous_hash)
        self._signature: Signature or None = None
        self.blockType = __name__
        self.dataForFunction = dataForFunction #Données pour faire toutes les vérifications et toutes les actions

        #Un array est utiliser plutôt qu'un dictionnaire pour avoir plusieurs functions avec le même nom
        self.verification = [] #Array contenant toutes les verifications à effectuer avant de valider le bloc. 
        self.action= [] #Toutes les actions réalisé par le bloc
  


    def __str__(self):
        result = ''
        result += f'previous hash: {self._header.previous_hash}\n'
        result += f'hash:          {self.hash}\n'
        result += f'timestamp:     {self._header.timestamp}\n'
        result += f'signed by:     {self._signature.signer if self.is_signed else "not yet signed"}\n\n'

        result += f'block type: {self.blockType}\n'
        result += f'verification list:\n' + indent(json.dumps(self.verification, indent=4), '\t') + '\n'

        #result += f'action done:\n' + indent(json.dumps(self.action, indent=4), '\t') + '\n'
        result += f'action done:\n'
        if len(self.action) == 0:
            result += f'    No action\n'
        else:
            for (func, parameters) in self.action:
                result += f'     {func.__name__}'

                for param in parameters:
                    result += f' {param}'

    
        result += '\n'
        result += f'data:\n' + indent(json.dumps(self.dataForFunction, indent=4), '\t') + '\n'

        result += f'balance:\n' + indent(json.dumps(self.balance, indent=4), '\t') + '\n'
        return result


    def addDataForFunction(self, dataName: str, value: any) -> 'Block_test':
        if self._signature is not None:
            raise Exception("Can't make change to a signed block. ")

        self.dataForFunction[dataName] = value
        return self

    def addVerification(self, verifName: str, verifFunction) -> 'Block_test':
        if self._signature is not None:
            raise Exception("Can't make change to a signed block. ")

        self.verification.append((verifName, verifFunction))
        return self
    

    def addAction(self, actionFunction, parametersName) -> 'Block_test':
        if self._signature is not None:
            raise Exception("Can't make change to a signed block. ")

        self.action.append((actionFunction, parametersName))
        return self


    def executeAllAction(self):
        for (actionFunction, parametersName) in self.action:
            self.executeAction(actionFunction, parametersName)


    def executeAction(self, actionFunction, parameters):
        actionToDO:str = actionFunction.__name__
        actionToDO += '(self,'

        for paramName in parameters:
            actionToDO += f' {self.dataForFunction[paramName]},'

        actionToDO += ')'

        print(actionToDO)
        eval(actionToDO)




    def sign(self, private_key: PrivateKey) -> None:
        if self._signature is not None:
            raise Exception("Block already signed. ")

        self._header.hash_root = sha(self.action)
        self._signature = sign(self.hash, private_key)


    def verify(self, public_key: PublicKey) -> bool:
        return (self.is_signed and
                self.verify_signature(public_key) and
                self._header.hash_root == sha(self.action))


    def verify_signature(self, public_key: PublicKey) -> bool:
        if self._signature is None:
            return False

        return self._signature.verify(self.hash, public_key)


    def is_previous_of(self, next_block: 'Block_test') -> bool:
        return self.hash == next_block._header.previous_hash




#Temporaire : En attendant de trouver une méthode pour régler les importations circulaire
def addCurrency(bloc: Block_test, unit: str, startingNumberOfCredit: int or float):
    bloc.balance[unit] = startingNumberOfCredit