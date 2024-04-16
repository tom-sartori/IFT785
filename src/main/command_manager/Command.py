from abc import abstractmethod, ABC


class Command(ABC):
    """
    The Command interface declares a method for executing a command.
    """

    def __init__(self, name, description, args):
        self.name = name
        self.description = description
        self.args = args

    @abstractmethod
    def execute(self) -> None:
        pass

    def get_help(self):
        return f"{self.name}: {self.description}\n  Args: {', '.join(self.args)}"
