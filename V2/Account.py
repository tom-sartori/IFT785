from textwrap import indent

from V2.Block import Block
from V2.OpenBlock import OpenBlock
from V2.fake_crypto import PublicKey, PrivateKey


class Account:

    def __init__(self, private_key: PrivateKey, public_key: PublicKey):
        # TODO: Chain class ?
        # TODO: Store private_key ?

        self.public_key = public_key

        block = OpenBlock(public_key)
        block.sign(private_key)
        self.chain: list[Block] = [block]

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    @property
    def balance(self) -> float:
        # TODO: Balance should also be stored in the ledger.
        for block in reversed(self.chain):
            if 'balance' in block.data:
                return block.data['balance']
        return 0.0

    def __str__(self):
        result = f'Chain of {self.public_key.owner}, with {len(self.chain)} blocks:\n'
        for block in self.chain:
            result += indent(block.__str__(), '\t')
            result += '\t---\n'

        return result

    def add_block(self, block: Block, private_key: PrivateKey) -> None:
        if not self.last_block.is_signed:
            raise Exception("Previous block must be signed. ")

        if not self.is_block_valid(block):
            raise Exception("Block must be added to the end of the chain. ")

        if block.is_signed:
            # Verify the signature.
            if not block.verify(self.public_key):
                raise Exception("Block signature verification failed. ")
        else:
            block.sign(private_key)

        self.chain.append(block)

    def is_block_valid(self, block: Block) -> bool:
        return block.previous_hash == self.last_block.hash

    @staticmethod
    def is_link_valid(previous_block: Block, next_block: Block, ) -> bool:
        return previous_block.hash == next_block.previous_hash

    def verify_chain(self) -> bool:
        for i in range(len(self.chain) - 1):
            block = self.chain[i]

            if not block.verify(self.public_key):
                print(f"Error: Block verification failed for {i}th block [{block.hash}]")
                return False
            if not self.is_link_valid(block, self.chain[i + 1]):
                print(f"Error: Chain verification failed between {i}th and {i + 1}th blocks")
                return False

        # The last block is not verified by the above loop.
        return self.chain[-1].verify(self.public_key)
