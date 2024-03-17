#!/usr/bin/env python
# 6 semaines 22 avril

# use python >= 3.7
import sys
assert sys.version_info >= (3, 7)


from fake_crypto import generate_keys, new_random_hash, new_deterministic_hash
from generic_block import GenericBlock
from chain import Chain











if __name__ == '__main__':

	alice = "Alice"
	alice_sk, alice_pk = generate_keys(alice)

	b1 = GenericBlock()
	#alice_genesis_block.sign(alice_sk)
	#alice_chain = Chain(alice_genesis_block)
