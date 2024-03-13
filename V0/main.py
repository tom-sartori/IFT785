#!/usr/bin/env python
# 6 semaines 22 avril

# use python >= 3.7
import sys

assert sys.version_info >= (3, 7)

from fake_crypto import generate_keys
from generic_block import GenericBlock

if __name__ == '__main__':
    alice = "Alice"
    alice_sk, alice_pk = generate_keys(alice)

    b1 = GenericBlock()
    print(b1)
# alice_genesis_block.sign(alice_sk)
# alice_chain = Chain(alice_genesis_block)
