from command_manager.Command import Command

from dsl.BlockTypeRegister import BlockTypeRegister

from dsl.Dsl import Dsl


class ShowBlocksCommand(Command):
    """
    Some commands can implement simple operations on their own.
    """

    def execute(self) -> None:
        dsl: Dsl = Dsl(dsl_file_name='resources/dsl.json')
        BlockTypeRegister().add_block_types(dsl.blocks)
        print(BlockTypeRegister())
