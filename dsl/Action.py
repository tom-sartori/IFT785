from SingletonMeta import SingletonMeta


class Action(metaclass=SingletonMeta):

    def __init__(self):
        self._methods: dict[str, callable] = dict()

    def __add__(self, method: callable):
        self._methods[method.__name__] = method
        return self

    def __getitem__(self, item: str):
        return self._methods[item]


def assign_balance_when_opening(block, account: str or None) -> None:
    if account is None or account == block.account_public_key:
        # The user take the money.
        print('account == account_public_key')
    else:
        # The user's balance is 0.
        block.data['balance'] = 0


Action().__add__(assign_balance_when_opening)

