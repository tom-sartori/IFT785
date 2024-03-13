from Account import Account
from Block import Block
from Chain import Chain
from GenesisBlock import GenesisBlock

if __name__ == '__main__':
    alice: Account = Account('Alice')

    alice_genesis_block = GenesisBlock()
    alice_genesis_block.sign(alice.private_key)

    alice_chain = Chain(alice, alice_genesis_block)
    print(alice_chain)

    block1 = Block(alice_genesis_block)
    block1.add_data('test', True)
    block1.sign(alice.private_key)

    alice_chain.add_block(block1)
    print(alice_chain)
