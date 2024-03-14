from V2.Account import Account
from V2.GenesisAccount import GenesisAccount
from V2.Ledger import Ledger
from V2.SendBlock import SendBlock
from V2.fake_crypto import generate_keys

if __name__ == '__main__':
    # TODO: User(username, private_key, public_key) class.
    # TODO: Constants file.

    ledger: Ledger = Ledger()

    genesis = 'Genesis'
    genesis_private_key, genesis_public_key = generate_keys(genesis)
    genesis_account = GenesisAccount(genesis_private_key, genesis_public_key)
    ledger.add_account(genesis_account)
    ledger.set_balance(genesis_account, genesis_account.last_block.data['balance'])  # TODO: Remove this line.

    alice = 'Alice'
    alice_private_key, alice_public_key = generate_keys(alice)
    alice_account = Account(alice_private_key, alice_public_key)
    ledger.add_account(alice_account)

    print(ledger)

    genesis_account.add_block(
        block=SendBlock(
            previous_block=genesis_account.last_block,
            balance=ledger.get_balance(genesis_account),
            destination=alice_account,
            amount=10.0
        ),
        private_key=alice_private_key
    )

    print(ledger)
