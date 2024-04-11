from Account import Account
from BlockTypeRegister import BlockTypeRegister
from Dsl import Dsl
from Ledger import Ledger
from fake_crypto import generate_keys
from to_generate.OpenBlock import OpenBlock

if __name__ == '__main__':
    dsl: Dsl = Dsl(dsl_file_name='dsl/dsl.json')
    # BlockTypeRegister().add_block_types(dsl.blocks)
    # print(BlockTypeRegister())

    genesis_account: Account = Account(*generate_keys('Genesis'))
    Ledger().add_account(genesis_account)

    second_account: Account = Account(*generate_keys('Second'))
    Ledger().add_account(second_account)

    print("Genesis account", genesis_account.head)

    open_block_genesis = OpenBlock(
        previous_block=genesis_account.head,
        unit='nano_coin',
        balance=1000,
        account=genesis_account.public_key.key
    )

    genesis_account.add_block(open_block_genesis)

    # open_nanocoin = BlockTypeRegister()['OpenNanocoin'](genesis_account.head)
    # genesis_account.add_block(open_nanocoin)

    # genesis_account.add_block(
    #     # 'previous_block', 'receiver', 'amount', and 'open_hash'
    #     BlockTypeRegister()['Send'](genesis_account.head, second_account.public_key.key, 50, open_nanocoin.hash)
    # )

    # print(Ledger())
