from command_manager.CommandFactory import CommandFactory


class Invoker:
    """
    The Invoker is associated with one or several commands. It sends a request
    to the command.
    """

    def __init__(self, command_input: str):
        self.command = CommandFactory()[command_input]

    def execute(self):
        if self.command:
            self.command.execute()
        else:
            print("Unknown command.")
