from V3.Account import Account
from V3.Ledger import Ledger
from V3.fake_crypto import generate_keys
from V3.to_generate.OpenBlock import OpenBlock

if __name__ == '__main__':
    ledger: Ledger = Ledger()

    genesis_account: Account = Account(*generate_keys('Genesis'))
    ledger.add_account(genesis_account)

    open_block_genesis = OpenBlock(
        previous_block=genesis_account.head,
        unit='nano_coin',
        balance=1000,
        account=genesis_account.public_key.key
    )

    genesis_account.add_block(open_block_genesis)

    print(ledger)
