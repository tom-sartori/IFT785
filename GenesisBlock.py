from Block import Block
from fake_crypto import PublicKey


class GenesisBlock(Block):

    def __init__(self, public_key: PublicKey):
        super().__init__(None)

        self._header.previous_hash = None
        self.account: str = public_key.key

    def __str__(self):
        result = ''
        result += f'public key: {self.account}\n'
        return result

    def on_sign_verification(self) -> bool:
        return True
