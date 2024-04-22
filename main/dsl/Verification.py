from main.ledger.Ledger import Ledger

from main.utils.SingletonMeta import SingletonMeta


class Verification(metaclass=SingletonMeta):

    def __init__(self):
        self._methods: dict[str, callable] = dict()

    def __add__(self, method: callable):
        self._methods[method.__name__] = method
        return self

    def __getitem__(self, item: str):
        return self._methods[item]


def is_superior(a, b) -> bool:
    return a > b


def is_equal(a, b) -> bool:
    return a == b


def account_exists(account_public_key: str) -> bool:
    return Ledger().get_account(account_public_key) is not None


def is_balance_valid(block: 'Block', open_hash: str) -> bool:
    open_block: 'Block' = Ledger().get_block(open_hash)
    minimal_balance = open_block.data['minimal_balance'] if 'minimal_balance' in open_block.data else 0
    return block.data['balance'] >= minimal_balance


Verification().__add__(is_superior)
Verification().__add__(is_equal)
Verification().__add__(account_exists)
Verification().__add__(is_balance_valid)
