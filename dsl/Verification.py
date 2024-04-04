from SingletonMeta import SingletonMeta


class Verification(metaclass=SingletonMeta):

    def __init__(self):
        self._methods: dict[str, callable] = dict()

    def __add__(self, method: callable):
        self._methods[method.__name__] = method
        return self

    def __getitem__(self, item: str):
        return self._methods[item]


def test_on_sign_verification() -> bool:
    print('on_sign_verification')
    return True


def is_superior(a, b) -> bool:
    return a > b


def is_equal(a, b) -> bool:
    return a == b


Verification().__add__(test_on_sign_verification)
Verification().__add__(is_superior)
Verification().__add__(is_equal)
