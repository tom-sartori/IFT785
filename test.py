import json

from Account import Account
from Block import Block
from Ledger import Ledger
from dsl.Verification import Verification
from fake_crypto import generate_keys


def init(self, previous_block, a, b):
    Block.__init__(self, previous_block)
    self.add_data('a', a)
    self.add_data('b', b)


def find_verification_method(method_name: str) -> callable:
    # TODO: If the method is not found.
    return Verification()[method_name]
    # for name, method in Verification.__dict__.items():
    #     if name == method_name:
    #         return method
    #
    # print(f'Error: Verification method {method_name} not found. ')
    # return None


if __name__ == '__main__':
    genesis_account: Account = Account(*generate_keys('Genesis'))
    Ledger().add_account(genesis_account)

    dsl = json.loads(open('dsl/dsl.json', 'r').read())
    block_str = dsl['blocks']['OpenNanocoin']

    SubBlock = type('SubBlock', (Block,), {
        '__init__': init,
        'data': block_str['data']
    })

    block = SubBlock(genesis_account.head, 5, 5)
    genesis_account.add_block(block)

    print(genesis_account)
