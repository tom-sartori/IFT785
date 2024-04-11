#!/usr/bin/env python


import hashlib

# example of hash
SEED = "9B322C7CA3A0175C44219844FF1BED422FBCEE4A"


def new_random_hash():
    """
    generate a random hash which can be used has genesis hash
    return an uppercase 40 lenght hex string (160 bits)
    """
    return sha(str(random.randrange(2 ** 256)))


def new_deterministic_hash():
    """
    generate a deterministic hash which can be used has genesis hash
    preferred for repeatability
    return an uppercase 40 lenght hex string (160 bits)
    """
    new_deterministic_hash.generated.append(sha(new_deterministic_hash.generated[-1]))
    return new_deterministic_hash.generated[-2]


new_deterministic_hash.generated = [SEED]


class Key:
    def __init__(self, owner: str) -> None:
        self.owner = owner
        self.key = ""

    def __str__(self) -> str:
        return self.__repr__()[1:-1]

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.key} of {self.owner}>"


class PublicKey(Key):
    def __init__(self, owner: str) -> None:
        super().__init__(owner)
        self.key = sha(sha(self.owner))


class PrivateKey(Key):
    def __init__(self, owner: str) -> None:
        super().__init__(owner)
        self.key = sha(self.owner)

    def public_key(self) -> PublicKey:
        return PublicKey(self.owner)


class Signature:

    @property
    def signer(self) -> str:
        return self._signer

    def __init__(self, message: str, private_key: PrivateKey) -> None:
        self._message = message
        self._signer = private_key.owner

    def verify(self, message: str, key: Key) -> bool:
        return self._message == message and self._signer == key.owner


def generate_keys(user: str) -> (PrivateKey, PublicKey):
    private_key = PrivateKey(user)
    public_key = private_key.public_key()
    return private_key, public_key


def sign(message: str, private_key: PrivateKey) -> Signature:
    if not isinstance(private_key, PrivateKey):
        raise Exception("Sign with private key.")
    return Signature(message, private_key)


def verify(message: str, signature: Signature, key: Key) -> bool:
    return signature.verify(message, key)


def sha(message):
    if not isinstance(message, str):
        message = str(message)
    return hashlib.sha1(message.encode('utf-8')).hexdigest().upper()
