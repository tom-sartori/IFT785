from V2.Account import Account
from V2.Block import Block
from V2.fake_crypto import generate_keys

if __name__ == '__main__':
    # TODO: User(username, private_key, public_key) class.
    # TODO: Constants file.

    alice = 'Alice'
    alice_private_key, alice_public_key = generate_keys(alice)

    alice_account = Account(alice_private_key, alice_public_key)
    print(alice_account)

    alice_account.add_block(
        block=Block(previous_block=alice_account.last_block, data={'open': True}),
        private_key=alice_private_key
    )
    print(alice_account)
