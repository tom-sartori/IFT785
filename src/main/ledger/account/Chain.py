from ledger.Ledger import Ledger
from ledger.block.Block import Block
from ledger.block.GenesisBlock import GenesisBlock
from utils.fake_crypto import PublicKey


class Chain:

    @property
    def head(self):
        return self._block_list[-1]

    def __init__(self, genesis_block: GenesisBlock):
        self._block_list: list[Block] = [genesis_block]

    def __str__(self):
        result = ''
        for block in self._block_list:
            result += block.__str__()
            result += '---\n'

        return result

    def __len__(self):
        return len(self._block_list)

    def add_block(self, block: Block, public_key: PublicKey) -> None:
        # The block must be signed before adding it to the chain.

        if not self.head.is_signed:
            raise Exception(f'Error: Head block must be signed. ')

        if not self.head.is_previous_of(next_block=block):
            raise Exception(f'Error: Block must be added to the end of the chain. ')

        if block.is_signed and not block.verify(public_key):
            raise Exception(f'Error: Block signature verification failed. ')

        self._block_list.append(block)

    def verify(self, public_key: PublicKey) -> bool:
        for i in range(len(self._block_list) - 1):
            block = self._block_list[i]

            if not block.verify(public_key):
                print(f"Error: Block verification failed for {i}th block [{block.hash}]")
                return False
            if not block.is_previous_of(next_block=self._block_list[i + 1]):
                print(f"Error: Chain verification failed between {i}th and {i + 1}th blocks")
                return False

        # The head block is not verified by the above loop.
        return self.head.verify(public_key)

    def get_balances(self) -> dict[str, int or float]:
        balances = dict()  # unit -> balance
        for block in reversed(self._block_list):
            if 'balance' in block.data:
                if 'unit' in block.data:
                    unit = block.data['unit']
                elif 'open_hash' in block.data:
                    open_block = Ledger().get_block(block.data['open_hash'])
                    unit = open_block.data['unit']
                else:
                    continue

                if unit not in balances:
                    balances[unit] = block.data['balance']

        return balances

    def get_balance(self, unit: str) -> int or float:
        balances = self.get_balances()
        if unit in balances:
            return balances[unit]
        else:
            raise Exception(f'Error: No balance found for unit {unit}. ')
