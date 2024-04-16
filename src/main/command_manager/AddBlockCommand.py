from command_manager.Command import Command

from command_manager.Receiver import Receiver


class AddBlockCommand(Command):
    """
    Some commands can implement simple operations on their own.
    """

    def __init__(self, receiver: Receiver, args: []) -> None:

        self._receiver = receiver
        self._args = args

    def execute(self) -> None:
        self._receiver.add_particular_block(self._args)
