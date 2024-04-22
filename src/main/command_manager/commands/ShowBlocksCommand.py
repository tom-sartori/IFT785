from command_manager.commands.Command import Command
from dsl.BlockTypeRegister import BlockTypeRegister


class ShowBlocksCommand(Command):
    """
    Some commands can implement simple operations on their own.
    """

    def execute(self) -> None:
        print(BlockTypeRegister())
