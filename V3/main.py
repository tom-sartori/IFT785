from V3.Account import Account
from V3.Ledger import Ledger
from V3.fake_crypto import generate_keys

if __name__ == '__main__':
    ledger: Ledger = Ledger()

    genesis_account: Account = Account(*generate_keys('Genesis'))
    ledger.add_account(genesis_account)

    print(ledger)
