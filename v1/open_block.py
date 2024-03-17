from fake_crypto import  generate_keys, sign, Signature
from user import user
from account import Account
# form  import GenericBlock
from generic_block import GenericBlock
class OpenBlock(GenericBlock):
    def __init__(self, account:Account, source,type, signature, representative= None):
        super.__init__()
        self.account = account
        self.source = source
        self.type = "OpenBlock"
        self.data = None
        self.signature = self.sign(account.getPrivateKey())