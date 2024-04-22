from command_manager.commands.Command import Command
from ledger.Ledger import Ledger
from ledger.account.Account import Account
from utils.fake_crypto import generate_keys


class CreateAccountCommand(Command):
    """
    Some commands can implement simple operations on their own.
    """

    def __init__(self, user_name: str) -> None:
        self.user_name = user_name

    def execute(self) -> None:
        self.__create_account(self.user_name)

    def __create_account(self, name):
        if self.__is_account_already_exist(str(name)):
            print("Account already exists. Please choose another name.")
        else:
            account = Account(*generate_keys(str(name)))
            Ledger().add_account(account)

    @staticmethod
    def __is_account_already_exist(name):
        return any(account.public_key.owner == name for account in Ledger().accounts.values())
