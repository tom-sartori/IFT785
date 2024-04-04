from Account import Account

from Ledger import Ledger
from fake_crypto import generate_keys
from to_generate.OpenBlock import OpenBlock

if __name__ == '__main__':
    genesis_account: Account = Account(*generate_keys('Genesis'))
    Ledger().add_account(genesis_account)

    open_block_genesis = OpenBlock(
        previous_block=genesis_account.head,
        unit='nano_coin',
        balance=1000,
        account=genesis_account.public_key.key
    )

    genesis_account.add_block(open_block_genesis)

    print(Ledger())

    # print(open_block_genesis.account_public_key)
    # print(Ledger().get_account(open_block_genesis.account_public_key))
    # print(Ledger().get_block(open_block_genesis.hash))
