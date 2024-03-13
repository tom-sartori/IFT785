from fake_crypto import generate_keys, PrivateKey


class Account:

    def __init__(self, username: str):
        self.username = username
        self._private_key, self._public_key = generate_keys(self.username)
        self._balance: float = 0

    @property
    def private_key(self) -> PrivateKey:
        return self._private_key

    @property
    def public_key(self) -> str:
        return self._public_key

    def add_balance(self, amount: float) -> float:
        self._balance += amount
        return self._balance

    def sub_balance(self, amount: float) -> float:
        self._balance -= amount
        return self._balance
