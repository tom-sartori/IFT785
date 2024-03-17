from fake_crypto import generate_keys

class User:
    def __init__(self, username: str):
        self.username = username
        (public_Key, private_Key) = generate_keys(self.username)
        self.__public_key = public_Key
        self.__private_key = private_Key
        
    def getPrivateKey(self):
        return self.__private_key
    
    def getPublicKey(self):
        return self.__public_key




user  =  User('Johan')
key   =user.getPrivateKey()
print(key.key)
