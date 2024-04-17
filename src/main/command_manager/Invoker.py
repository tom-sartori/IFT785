from command_manager.Command import Command


class Invoker:
    """
    The Invoker is associated with one or several commands. It sends a request
    to the command.
    """

    _on_start = None
    _on_finish = None

    """
    Initialize commands.
    """

    def __init__(self):
        self.commands = {}

    def register_command(self, command_name, command: Command):
        self.commands[command_name] = command

    def execute_command(self, command_name):
        if command_name in self.commands:
            if isinstance(self.commands[command_name], Command):
                self.commands[command_name].execute()
        else:
            print("Command not recognized.")
