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


def set_balance(block: 'Block', block_hash: str) -> None:
    retrieved_block: 'Block' = Ledger().get_block(block_hash)

    if 'unit' in retrieved_block.data:
        # The block is an open block.
        unit = retrieved_block.data['unit']
    elif 'open_hash' in retrieved_block.data:
        # The block is a send block.
        open_block = Ledger().get_block(retrieved_block.data['open_hash'])
        unit = open_block.data['unit']
    else:
        raise ValueError('The block is not an open or send block. Unable to set the balance.')

    balance = Ledger().get_account(block.account_public_key).get_balance(unit)
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


def set_amount(block: 'Block', send_hash: str) -> None:
    send_block: 'Block' = Ledger().get_block(send_hash)
    block.data['amount'] = send_block.data['amount']


def set_open_hash(block: 'Block', other_block_hash: str) -> None:
    other_block: 'Block' = Ledger().get_block(other_block_hash)
    block.data['open_hash'] = other_block.data['open_hash']


Action().__add__(assign_balance_when_opening)
Action().__add__(set_balance)
Action().__add__(decrease_balance)
Action().__add__(increase_balance)
Action().__add__(set_amount)
Action().__add__(set_open_hash)
