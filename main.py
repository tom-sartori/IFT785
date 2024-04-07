from Account import Account

from Ledger import Ledger
from fake_crypto import generate_keys,PublicKey
from to_generate.OpenBlock import OpenBlock
from to_generate.SendBlock import SendBlock
from to_generate.ReceiveBlock import ReceiveBlock


if __name__ == '__main__':
    genesis_account: Account = Account(*generate_keys('Genesis'))
    Ledger().add_account(genesis_account)

    open_block_genesis = OpenBlock(
        previous_block=genesis_account.head,
        unit='nano-coin',
        balance=1000,
        account=genesis_account.public_key.key
    )

    genesis_account.add_block(open_block_genesis)

    print(ledger)
