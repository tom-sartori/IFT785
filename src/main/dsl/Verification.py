from ledger.Ledger import Ledger
from utils.SingletonMeta import SingletonMeta


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
    print("Account exists method called")
    return Ledger().get_account(account_public_key) is not None


def is_balance_valid(block: 'Block', open_hash: str) -> bool:
    open_block: 'Block' = Ledger().get_block(open_hash)
    minimal_balance = open_block.data['minimal_balance'] if 'minimal_balance' in open_block.data else 0
    return block.data['balance'] >= minimal_balance

def open_block_does_not_exist(block:'Block') -> bool:
    account_public_key = block.account_public_key
    if account_public_key is None or not account_exists(account_public_key):
        # raise error account must be specified
        raise ValueError("Cannot be null")
    
    # checker si le unit existe dans le account chain
    account = Ledger().get_account(account_public_key)
    balance = account.get_balance(block.data['unit'])
    return True if balance is None else False

def can_interact_with(block:'Block',open_hash:str) -> bool:
    open_block = Ledger().get_block(open_hash)
    if block.data['block_type'] in open_block.data['interact_with']:
        return True
    else:
        raise Exception("You can't interact with this open block")
        return False
    
def is_divisible(open_hash:str) -> bool:
    open_block = Ledger().get_block(open_hash)
    return open_block.data['divisible'] if 'divisible' in open_block.data else True

Verification().__add__(is_superior)
Verification().__add__(is_equal)
Verification().__add__(account_exists)
Verification().__add__(is_balance_valid)
Verification().__add__(open_block_does_not_exist)
Verification().__add__(can_interact_with)