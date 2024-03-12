from Chain import Chain
from GenesisBlock import GenesisBlock
from fake_crypto import generate_keys

if __name__ == '__main__':
    alice = "Alice"
    alice_secrete_key, alice_private_key = generate_keys(alice)

    alice_genesis_block = GenesisBlock()
    alice_genesis_block.sign(alice_secrete_key)

    alice_chain = Chain(alice_genesis_block)
    print(alice_chain)
