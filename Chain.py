from textwrap import indent

from Block import Block


class Chain:

    def __init__(self, genesis_block: Block):
        """
        initialized Chain object with genesis_block
        """

        # TODO: Make a class genesis_block.

        if not isinstance(genesis_block, Block):
            raise Exception("Chain must be initialized with a genesis Block. ")

        self._block_list = [genesis_block]

    def __str__(self):
        result = f'Chain with {len(self._block_list)} blocks:\n'
        for block in self._block_list:
            result += indent(block.__str__(), '\t')

        return result

    def __repr__(self):
        """
        Chain representation
        """
        return f"<{type(self).__name__}>"

    def verify(self, public_key):
        for i in range(len(self._block_list) - 1):
            block = self._block_list[i]
            if not block.verify_data():
                # raise Exception(f"Data verification failed for {i}th block : H={block.hash()}")
                print(f"Error: Data verification failed for {i}th block [{block.hash}]")
                return False
            if not block.verify_signature(public_key):
                # raise Exception(f"Signature verification failed for {i}th block : H={block.hash()}")
                print(f"Error: Signature verification failed for {i}th block [{block.hash}]")
                return False
            if block.hash != self._block_list[i + 1].header.previous_hash:
                # raise Exception(f"Chain verification failed between {i}th and {i+1}th blocks")
                print(f"Error: Chain verification failed between {i}th and {i + 1}th blocks")
                return False

        block = self._block_list[-1]
        if not block.verify_data():
            print(f"Warning: Data verification failed for last block [{block.hash}]")
            return False
        if not block.verify_signature(public_key):
            print(f"Warning: Signature verification failed for last block [{block.hash}]")
            return False

        return True

    def add_block(self, block: Block) -> None:
        if not isinstance(block, Block):
            raise Exception("Chain must be added with a Block. ")
        if block.header.previous_hash != self._block_list[-1].hash:
            raise Exception("Block must be added to the end of the chain. ")
        self._block_list.append(block)
