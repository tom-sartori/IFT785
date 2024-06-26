from main.ledger.Ledger import Ledger

from main.utils.SingletonMeta import SingletonMeta


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

    if 'open_hash' in retrieved_block.data:
        # The block is a send block.
        retrieved_block = Ledger().get_block(retrieved_block.data['open_hash'])
    if 'unit' in retrieved_block.data:
        # The block is an open block.
        unit = retrieved_block.data['unit']
    else:
        raise ValueError('The block is not an open or send block. Unable to set the balance.')
    balance = Ledger().get_account(block.account_public_key).get_balance(unit)
    block.data['balance'] = balance


def decrease_balance(block: 'Block', amount: int or float, amount_fee: float = 0) -> None:
    """
    Precondition: block.data['balance'] is not None.

    :param block: the block to decrease the balance.
    :param amount: the amount to decrease.
    :param amount_fee: the amount of fee to decrease.
    :return: None
    """
    amount = float(amount)
    amount_fee = float(amount_fee)

    if 'open_hash' in block.data:
        open_block = Ledger().get_block(block.data['open_hash'])
        if '_is_divisible' in open_block.data and not open_block.data['_is_divisible']:
            amount = int(amount)

    block.data['balance'] = block.data['balance'] - amount - amount_fee


def increase_balance(block: 'Block', amount: int or float) -> None:
    """
    Precondition: block.data['balance'] is not None.

    :param block: the block to increase the balance.
    :param amount: the amount to increase.
    :return: None
    """
    amount = float(amount)

    if 'open_hash' in block.data:
        open_block = Ledger().get_block(block.data['open_hash'])
        if '_is_divisible' in open_block.data and not open_block.data['_is_divisible']:
            amount = int(amount)
    block.data['balance'] = block.data['balance'] + amount


def set_data_from_other_block_hash(block: 'Block', other_block_hash: str, data_key: str) -> None:
    other_block: 'Block' = Ledger().get_block(other_block_hash)
    block.data[data_key] = other_block.data[data_key]


def send(block: 'Block', amount: int or float, open_hash: str) -> None:
    set_balance(block, open_hash)
    decrease_balance(block, amount)


def send_with_fee(block: 'Block', amount: int or float, open_hash: str) -> None:
    set_balance(block, open_hash)
    transaction_fee = Ledger().get_block(open_hash).data['transaction_fee']
    amount_fee = _transaction_amount_fee(transaction_fee, amount)
    decrease_balance(block, amount, amount_fee)


def receive(block: 'Block', send_hash: str) -> None:
    set_balance(block, send_hash)
    set_data_from_other_block_hash(block, send_hash, 'open_hash')

    amount = Ledger().get_block(send_hash).data['amount']
    increase_balance(block, amount)


def _transaction_amount_fee(transaction_fee, amount):
    return amount * transaction_fee


def _is_divisible(open_hash: str) -> bool:
    open_block = Ledger().get_block(open_hash)
    return open_block.data['is_divisible'] if 'is_divisible' in open_block.data else True


Action().__add__(assign_balance_when_opening)
Action().__add__(set_balance)
Action().__add__(decrease_balance)
Action().__add__(increase_balance)
Action().__add__(set_data_from_other_block_hash)
Action().__add__(send)
Action().__add__(send_with_fee)
Action().__add__(receive)
