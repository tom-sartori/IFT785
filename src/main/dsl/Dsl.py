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
        # TODO
        print("block_definition is ", block_definition)

        # if not block_definition['block_type'] in self.documentation['blocks'].keys():
        #     print(f'Error: Block type {block_definition["block_type"]} not in documentation. ')
        #     return False
        # block_documentation = self.documentation['blocks'][block_definition['block_type']]
        # print("block_documentation is ", block_documentation)
        # print("block_definition is ", block_definition)
        
        # if block_documentation is None:
        #     print(f'Error: Block type {block_definition["block_type"]} has no documentation. ')
        #     return False
      
        #
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
        return False
