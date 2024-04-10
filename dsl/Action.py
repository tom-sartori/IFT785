from Ledger import Ledger
from SingletonMeta import SingletonMeta


class Action(metaclass=SingletonMeta):

    def __init__(self):
        self._methods: dict[str, callable] = dict()

    def __add__(self, method: callable):
        self._methods[method.__name__] = method
        return self

    def __getitem__(self, item: str):
        return self._methods[item]


def assign_balance_when_opening(block: 'Block', account: str or None) -> None:
    if account is None or account == block.account_public_key:
        # The user take the money.
        pass
    else:
        # The user's balance is 0.
        block.data['balance'] = 0


def set_balance(block: 'Block', open_hash: str) -> None:
    open_block: 'Block' = Ledger().get_block(open_hash)
    account: 'Account' = Ledger().get_account(block.account_public_key)
    balance = account.get_balance(open_block.data['unit'])
    block.data['balance'] = balance


def decrease_balance(block: 'Block', amount: int or float) -> None:
    """
    Precondition: block.data['balance'] is not None.

    :param block: the block to decrease the balance.
    :param amount: the amount to decrease.
    :return: None
    """
    block.data['balance'] = block.data['balance'] - amount


def increase_balance(block: 'Block', amount: int or float) -> None:
    """
    Precondition: block.data['balance'] is not None.

    :param block: the block to increase the balance.
    :param amount: the amount to increase.
    :return: None
    """
    block.data['balance'] = block.data['balance'] + amount


Action().__add__(assign_balance_when_opening)
Action().__add__(set_balance)
Action().__add__(decrease_balance)
Action().__add__(increase_balance)
