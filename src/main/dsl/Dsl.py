import json
import os

class Dsl:

    def __init__(self, dsl_file_name: str):
        """
        Initializes the DSL. If the DSL is not verified, an exception is raised.

        :param dsl_file_name: str the name of the DSL file.
        """
        current_directory = os.getcwd()
        self.documentation = json.loads(open(current_directory + '/resources/documentation.json', 'r').read())
        self._dsl = json.loads(open(dsl_file_name, 'r').read())
        # print("Documentation is ", self.documentation)
        # print("dsl is ", self._dsl)
        if not self._is_verified():
            raise Exception('DSL is not verified. ')
        else:
            print('DSL is verified. ')

    @property
    def blocks(self) -> dict:
        """
        Returns the blocks of the DSL.
        :return: dict the blocks.
        """
        return self._dsl['blocks']

    def _is_verified(self) -> bool:
        """
        Verifies if the dsl respect the documentation.

        :return: bool True if the dsl is verified, False otherwise.
        """
        return self._arr_block_definitions_verified()

    def _arr_block_definitions_verified(self) -> bool:
        """
        Verifies if all block definitions are verified.

        :return: bool True if all block definitions are verified, False otherwise.
        """
        return all([self._is_block_definition_verified(block_definition)
                    for block_definition in self._dsl['blocks'].values()])

    def _is_block_definition_verified(self, block_definition: dict) -> bool:
        """
        Verifies if a block definition respect the documentation.

        :param block_definition: dict the block definition.
        :return: bool True if the block definition is verified, False otherwise.
        """

        # block_documentation = self.documentation['blocks']['Open'] \
        #     if self._is_open__block(block_definition) else self.documentation['blocks']['GenericBloc']
        #
        # if block_documentation is None:
        #     print(f'Error: Block type {block_definition["block_type"]} has no documentation. ')
        #     return False
        #
        # # TODO: For block_documentation.keys().
        # # TODO: Can't have is_divisible and transaction_fee.
        # for key in block_definition.keys():
        #     if key not in block_documentation.keys():
        #         print(f'Error: Block type {block_definition["block_type"]} has unknown key {key}. ')
        #         return False
        #
        #     documentation_attributes = block_documentation[key]
        #     key_is_required = documentation_attributes['required']
        #     if key_is_required and key not in block_definition.keys():
        #         print(f'Error: Block type {block_definition["block_type"]} has missing key {key}. ')
        #         return False
        #
        #     # Par defaut attribute_type est secable donc int or float sont vrai
        #     attribute_type = eval(documentation_attributes['type'])
        #     if documentation_attributes["type"] == 'int or float':
        #         attribute_type = (int, float)
        #
        #     # If the attribute is not divisible, it must be an int
        #     if "is_divisible" in block_definition.keys() and block_definition["is_divisible"] is False :
        #         attribute_type = int
        #
        #     if not isinstance(block_definition[key], attribute_type) and not isinstance(block_definition[key], type(None)):
        #         print(type(block_definition[key]))
        #         print(attribute_type)
        #         # print(documentation_attributes["type"])
        #         print(f'Error: Block type {block_definition["block_type"]} has wrong type for key {key} with value {block_definition[key]}. ')
        #         return False

        # if block_documentation.keys() != block_definition.keys():
        #     print(f'Error: Block type {block_definition["block_type"]} has different keys than the documentation. ')
        #     return False
        #
        # for key, value in block_documentation.items():
        #     attribute = block_definition[key]
        #
        #     # Check type.
        #     if not isinstance(attribute, eval(value['type'])):
        #         print(f'Error: Block type {block_definition["block_type"]} has wrong type for key {key}. ')
        #         return False
        #
        #     if 'value' in value.keys() and value['value'] != attribute:
        #         print(f'Error: Block type {block_definition["block_type"]} has wrong value for key {key}. ')
        #         return False

        # return True
        return True

    @staticmethod
    def _is_open__block(block_definition: dict) -> bool:
        """
        Verifies if a block definition is an open block.

        :param block_definition: str the block definition.
        :return: bool True if the block definition is an open block, False otherwise.
        """
        return 'interact_with' in block_definition.keys()

'''
block definition : {'unit': 'Nanocoin', 'balance': 100, 'minimal_balance': 0, 'on_sign_actions': [{'method_name': 'assign_balance_when_opening', 'args': ['self', 'account']}], 'on_sign_verifications': [{'method_name': 'open_block_does_not_exist', 'args': ['self']}], 'interact_with': []}

block definition : {'balance': None, 'open_hash': None, 'on_sign_actions': [{'method_name': 'send', 'args': ['self', 'amount', 'open_hash']}], 'on_sign_verifications': [{'method_name': 'account_exists', 'args': ['receiver']}, {'method_name': 'is_balance_valid', 'args': ['self', 'open_hash']}], 'parameters': ['receiver', 'amount', 'open_hash']}

block definition : {'balance': None, 'open_hash': None, 'on_sign_actions': [{'method_name': 'receive', 'args': ['self', 'send_hash']}], 'parameters': ['send_hash']}

'''

