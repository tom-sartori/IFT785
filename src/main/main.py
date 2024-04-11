from dsl.BlockTypeRegister import BlockTypeRegister
from dsl.Dsl import Dsl
from ledger.Ledger import Ledger
from ledger.account.Account import Account
from Interpreter import Interpreter
from utils.fake_crypto import generate_keys

if __name__ == '__main__':
    # Load the DSL and create the block types.
    # dsl: Dsl = Dsl(dsl_file_name='resources/dsl.json')
    # BlockTypeRegister().add_block_types(dsl.blocks)
    # print(BlockTypeRegister())
    #
    # # Create two accounts.
    # genesis_account: Account = Account(*generate_keys('Genesis'))
    # Ledger().add_account(genesis_account)
    # second_account: Account = Account(*generate_keys('Second'))
    # Ledger().add_account(second_account)
    #
    # # Open Nanocoin for Genesis.
    # genesis_open_nanocoin = BlockTypeRegister()['OpenNanocoin'](genesis_account.head)
    # genesis_account.add_block(genesis_open_nanocoin)
    #
    # # Open Nanocoin for Second.
    # second_account.add_block(BlockTypeRegister()['OpenNanocoin'](second_account.head))
    #
    # # Send 50 Nanocoins from Genesis to Second.
    # send_block = BlockTypeRegister()['Send'](
    #     previous_block=genesis_account.head,
    #     receiver=second_account.public_key.key,
    #     amount=40,
    #     open_hash=genesis_open_nanocoin.hash)
    # genesis_account.add_block(send_block)
    #
    # # Receive Nanocoins from Genesis to Second.
    # receive_block = BlockTypeRegister()['Receive'](previous_block=second_account.head, send_hash=send_block.hash)
    # second_account.add_block(receive_block)
    #
    # print(Ledger())
    #
    # print(genesis_account.balances)
    # print(second_account.balances)
    interpreter = Interpreter()

    """
            uncomment the following lines and run main.py to do a quick test or run the main in interpreter mode.
    """

    # interpreter.create_account("Alice")
    # interpreter.create_account("Bob")
    #
    # # Create Alice Account
    # interpreter.create_open_block(
    #     "4A20360DF0FDC9979B30BCB50318521E4DC9C05F",
    #     "OpenNanocoin",
    #     "Nanocoin",
    #     200,
    #     0
    # )
    #
    # # Create Bob Account
    # interpreter.create_open_block(
    #     "9AF3883DC6725FBF664400A8FA2C2F7FD6998629",
    #     "OpenNanocoin",
    #     "Nanocoin",
    #     200,
    #     0
    # )
    #
    # # send 25 from Alice to Bob
    # interpreter.create_send_block(
    #     "4A20360DF0FDC9979B30BCB50318521E4DC9C05F",
    #     "9AF3883DC6725FBF664400A8FA2C2F7FD6998629",
    #     25
    # )
    #
    # # Receive 25 Nanocoins from Alice.
    # interpreter.create_receive_block(
    #     "9AF3883DC6725FBF664400A8FA2C2F7FD6998629",
    #     "4A20360DF0FDC9979B30BCB50318521E4DC9C05F"
    # )
