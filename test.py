import json
from array import array

from Account import Account
from Block import Block
from Ledger import Ledger
from dsl.Verification import Verification
from fake_crypto import generate_keys


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
    print(block_str['attributes'])

    string = f"def init(self, previous_block, {', '.join(block_str['attributes'])}):"
    string += """
    Block.__init__(self, previous_block)

    my_dict = {k: v for k, v in locals().items() if isinstance(v, int) or isinstance(v, str)}
    for key, value in my_dict.items():
        self.add_data(key, value)
    """
    compiled = compile(string, '', 'exec')
    eval(compiled)

    SubBlock = type('SubBlock', (Block,), {
        '__init__': init,
        'data': block_str['data']
    })

    # block = SubBlock(genesis_account.head, {'a': 5, 'b': 5})
    block = SubBlock(genesis_account.head, 5, 5)
    genesis_account.add_block(block)

    # print(genesis_account)
