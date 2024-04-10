import json

from Account import Account
from BlockTypeRegister import BlockTypeRegister
from Ledger import Ledger
from fake_crypto import generate_keys

if __name__ == '__main__':
    dsl = json.loads(open('dsl/dsl.json', 'r').read())
    BlockTypeRegister().add_block_types(dsl['blocks'])
    print(BlockTypeRegister())

    genesis_account: Account = Account(*generate_keys('Genesis'))
    Ledger().add_account(genesis_account)

    block = BlockTypeRegister()['OpenNanocoin'](genesis_account.head, 5, 5)
    genesis_account.add_block(block)

    # print(genesis_account)
