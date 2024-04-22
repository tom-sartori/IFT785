from command_manager.Invoker import Invoker

if __name__ == "__main__":
    Invoker('help').execute()
    Invoker('create_account Jean').execute()
    Invoker('create_account Denis').execute()

    while True:
        command_input: str = input("\nEnter command: ")

        if command_input == "exit":
            print("Bye...")
            break

        Invoker(command_input).execute()
