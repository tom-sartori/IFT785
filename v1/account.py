from fake_crypto import generate_keys
from user import User
class Account:
    def __init__(self, user:User, account_name:str) -> None:
        self.user = user
        self.account_name = account_name
        self.public_key  = user.getPublicKey()
        self.private_key = user.getPrivateKey()