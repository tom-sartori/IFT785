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

        block_documentation = self.documentation['blocks']['Open'] \
            if self._is_open__block(block_definition) else self.documentation['blocks']['GenericBloc']
        
        if block_documentation is None:
            print(f'Error: Block type has no documentation. ')
            return False
        
        is_divisible = block_definition["is_divisible"] if "is_divisible" in block_definition.keys() else True
        if "transaction_fee" in block_definition.keys() and not is_divisible :
                print(f'Error: Block {block_definition["unit"]} Cannot have transaction_fee and not divisible (is_divisible: false). Note that by default is_divisible is true, so you have to set it explicitly to false otherwise. ')
                return False
        
        # If the attribute is not divisible, it must be an int
        is_divisible_type = (int, float)
        if not is_divisible :
            is_divisible_type = int
            '''
            {
                "is_divisible": false,
                "transaction_fee": 0.1
            }
            test_transaction_fee_and_is_divisible_cannot_work_together():
            
            '''
        # # TODO: For block_documentation.keys().
        # # TODO: Can't have is_divisible and transaction_fee.
        for key in block_definition.keys():
        
            documentation_attributes: dict = block_documentation[key]
            key_is_required: bool = documentation_attributes['required']
            
            if key_is_required and key not in block_definition.keys():
                print(f'Error: Block type {block_definition} has missing key {key}. ')
                return False
        
            # Par defaut attribute_type est secable donc int or float sont vrai
            attribute_type = eval(documentation_attributes['type'])
            if documentation_attributes["type"] == 'int or float':
                attribute_type = is_divisible_type
            
            if not isinstance(block_definition[key], attribute_type) and not isinstance(block_definition[key], type(None)):
                print(type(block_definition[key]))
                print(attribute_type)
                # print(documentation_attributes["type"])
                print(f'Error: Block type {block_definition} has wrong type for key {key} with value {block_definition[key]}. ')
                return False

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
