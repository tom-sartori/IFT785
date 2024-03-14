from V2.Account import Account
from V2.GenesisBlock import GenesisBlock
from V2.fake_crypto import PrivateKey, PublicKey


class GenesisAccount(Account):

    def __init__(self, private_key: PrivateKey, public_key: PublicKey):
        super().__init__(private_key, public_key)

        genesis_block = GenesisBlock()
        genesis_block.sign(private_key)
        self.chain[0] = genesis_block
