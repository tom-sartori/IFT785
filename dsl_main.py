import json

from Block import Block
from GenesisBlock import GenesisBlock
from fake_crypto import PublicKey, PrivateKey
from dsl.Verification import Verification

global documentation


def is_block_definition_verified(block_definition: dict) -> bool:
    if not block_definition['block_type'] in documentation['blocks'].keys():
        print(f'Error: Block type {block_definition["block_type"]} not in documentation. ')
        return False
    block_documentation = documentation['blocks'][block_definition['block_type']]

    if block_documentation is None:
        print(f'Error: Block type {block_definition["block_type"]} has no documentation. ')
        return False

    if block_documentation.keys() != block_definition.keys():
        print(f'Error: Block type {block_definition["block_type"]} has different keys than the documentation. ')
        return False

    for key, value in block_documentation.items():
        attribute = block_definition[key]

        # Check type.
        if not isinstance(attribute, eval(value['type'])):
            print(f'Error: Block type {block_definition["block_type"]} has wrong type for key {key}. ')
            return False

        if 'value' in value.keys() and value['value'] != attribute:
            print(f'Error: Block type {block_definition["block_type"]} has wrong value for key {key}. ')
            return False

    return True


def find_verification_method(method_name: str) -> callable:
    for name, method in Verification.__dict__.items():
        if name == method_name:
            return method

    print(f'Error: Verification method {method_name} not found. ')
    return None


if __name__ == '__main__':
    genesis_block = GenesisBlock(public_key=PublicKey('Genesis'))

    # Load the documentation and the DSL.
    documentation = json.loads(open('dsl/documentation.json', 'r').read())
    dsl = json.loads(open('dsl/dsl.json', 'r').read())

    blocks = dict()

    # Iterate over the blocks in the DSL.
    for block_name, block_definition in dsl['blocks'].items():
        if not is_block_definition_verified(block_definition):
            print(f'Error: Block definition {block_definition} does not respect the documentation. ')
            continue

        # Find the verification method defined in the DSL.
        on_sign_verification = find_verification_method(block_definition['on_sign_verification'])
        if on_sign_verification is None:
            continue

        # type(name, bases, attrs)
        #   - name: name of the class
        #   - bases: tuple of the parent class (for inheritance, can be empty)
        #   - attrs: dictionary containing attributes names and values
        BlockType = type(block_name, (Block,), {
            'on_sign_verification': on_sign_verification
        })

        # Create an instance of the block.
        block = BlockType(previous_block=genesis_block)
        for key, value in block_definition.items():
            block.add_data(key, value)

        blocks[block_name] = block
        block.sign(PrivateKey(''))

    for block_name, block in blocks.items():
        print(f'----- {block_name} -----\n')
        print(block)
        print()
