from command_manager.Invoker import Invoker
from command_manager.Receiver import Receiver
from command_manager.CommandFactory import CommandFactory
from dsl.BlockTypeRegister import BlockTypeRegister


def main():
    receiver = Receiver()
    invoker = Invoker()
    factory = CommandFactory(invoker, receiver)

    while True:
        command_input = input("Enter command: ")
        if command_input == "exit":
            print("Bye...")
            break

        command = factory.get_command(command_input)
        if command:
            invoker.register_command(command_input, command)
            invoker.execute_command(command_input)
        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()


