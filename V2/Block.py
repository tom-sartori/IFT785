from datetime import datetime

from V2.fake_crypto import new_deterministic_hash, sha, Signature, PublicKey, PrivateKey, sign


class Block:

    def __init__(self, previous_block: 'Block' = None, data: dict = None):
        # TODO: Header class ?

        if previous_block is None:
            self.previous_hash: str = new_deterministic_hash()
        elif isinstance(previous_block, Block):
            self.previous_hash: str = previous_block.hash
        else:
            raise Exception("previous_block must be Block or None. ")

        self._signature: Signature or None = None
        self.data = data if data else dict()
        self.timestamp = datetime.now()

    @property
    def hash(self) -> str:
        return sha((self.previous_hash, self.data))

    @property
    def is_signed(self) -> bool:
        return self._signature is not None

    def __str__(self) -> str:
        rop = ""
        rop += f"previous hash: {self.previous_hash}\n"
        rop += f"hash:          {self.hash}\n"
        rop += f"timestamp:     {self.timestamp}\n"
        rop += f"signed by:     {self._signature._signer}\n" if self.is_signed else "not yet signed\n"
        rop += f"data:          {self.data}\n"
        return rop

    def add_data(self, new_key: str, new_value: any) -> None:
        if self._signature is not None:
            raise Exception("Can't add data to a signed block. ")

        self.data[new_key] = new_value

    def add_data_and_sign(self, new_key: str, new_value: any, private_key) -> None:
        self.add_data(new_key, new_value)
        self.sign(private_key)

    def sign(self, private_key: PrivateKey) -> None:
        if self._signature is not None:
            raise Exception("Block already signed. ")

        self._signature = sign(self.hash, private_key)

    def verify(self, public_key: PublicKey) -> bool:
        return self._signature.verify(self.hash, public_key)
