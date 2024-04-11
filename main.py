from Account import Account
from BlockTypeRegister import BlockTypeRegister
from Dsl import Dsl
from Ledger import Ledger
from fake_crypto import generate_keys

if __name__ == '__main__':
    # Load the DSL and create the block types.
    dsl: Dsl = Dsl(dsl_file_name='dsl/dsl.json')
    BlockTypeRegister().add_block_types(dsl.blocks)
    print(BlockTypeRegister())

    # Create two accounts.
    genesis_account: Account = Account(*generate_keys('Genesis'))
    Ledger().add_account(genesis_account)
    second_account: Account = Account(*generate_keys('Second'))
    Ledger().add_account(second_account)

    # Open Nanocoin for Genesis.
    genesis_open_nanocoin = BlockTypeRegister()['OpenNanocoin'](genesis_account.head)
    genesis_account.add_block(genesis_open_nanocoin)

    # Open Nanocoin for Second.
    second_account.add_block(BlockTypeRegister()['OpenNanocoin'](second_account.head))

    # Send 50 Nanocoins from Genesis to Second.
    send_block = BlockTypeRegister()['Send'](
        previous_block=genesis_account.head,
        receiver=second_account.public_key.key,
        amount=40,
        open_hash=genesis_open_nanocoin.hash)
    genesis_account.add_block(send_block)

    # Receive Nanocoins from Genesis to Second.
    receive_block = BlockTypeRegister()['Receive'](previous_block=second_account.head, send_hash=send_block.hash)
    second_account.add_block(receive_block)

    print(Ledger())

    print(genesis_account.balances)
    print(second_account.balances)
