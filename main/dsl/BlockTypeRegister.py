import inspect

from main.dsl.Dsl import Dsl
from main.ledger.block.Block import Block
from main.utils.SingletonMeta import SingletonMeta


class BlockTypeRegister(metaclass=SingletonMeta):
    """
    This class is a singleton that holds all the block types.
    """

    def __init__(self):
        """
        Initializes the block type register.
        """
        self._block_types_dict: dict[str, type(Block)] = dict()

        # Load the DSL and create the block types.
        dsl: Dsl = Dsl(dsl_file_name='resources/dsl.json')
        self.add_block_types(dsl.blocks)

    def __add__(self, block_type: type(Block)) -> 'BlockTypeRegister':
        """
        Adds a block type to the register.

        :param block_type: type(Block) the block type to add.
        :return: BlockTypeRegister the register.
        """
        self._block_types_dict[block_type.__name__] = block_type
        return self

    def __getitem__(self, item: str) -> type(Block):
        """
        Gets a block type from the register.

        :param item: str the name of the block type.
        :return: type(Block) the block type.
        """
        return self._block_types_dict[item]

    def __str__(self) -> str:
        """
        Returns a string representation of the block types.

        :return: str the string representation. Like:
            - OpenNanocoin(previous_block, amount, recipient)
        """
        result = 'Available block types:\n'
        for key, value in self._block_types_dict.items():
            params = inspect.signature(value.__init__).parameters
            params = list(params.keys())[1:]  # Remove self.
            result += f'- {key}({", ".join(params)})\n'
        return result

    def add_block_types(self, block_types: dict[str, dict]) -> None:
        """
        Adds multiple block types to the register.

        :param block_types: dict[str, dict] the block names and their definitions. Usually from a DSL.
        :return: None
        """
        for block_name, block_str in block_types.items():
            self.add_block_type_from_str(block_name, block_str)

    def add_block_type_from_str(self, block_name: str, block_str: str) -> None:
        """
        Adds a block type to the register from a string.

        :param block_name: str name of the block type to create.
        :param block_str: str the block type definition.
        :return: None
        """
        parameters = block_str['parameters'] if 'parameters' in block_str.keys() else []

        SubBlockType = type(block_name, (Block,), {
            '__init__': self._get_init_function(parameters),
            'data': block_str
        })

        self.__add__(SubBlockType)

    @staticmethod
    def _get_init_function(parameters: list[str]) -> callable:
        """
        Creates and returns an init function for a block type class.

        :param parameters: list[str] the parameters of the block type.
        :return: callable the init function.
        """
        string = f"def init(self, previous_block, {', '.join(parameters)}):"
        string += """
        Block.__init__(self, previous_block)

        my_dict = {k: v for k, v in locals().items() if isinstance(v, int) or isinstance(v, str)}
        for key, value in my_dict.items():
            self.add_data(key, value)
        """
        compiled = compile(string, '', 'exec')
        eval(compiled)

        return locals()['init']
