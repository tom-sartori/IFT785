from command_manager.Command import Command

from ledger.Ledger import Ledger
from ledger.account.Account import Account
from utils.fake_crypto import generate_keys


class CreateAccountCommand(Command):
    """
    Some commands can implement simple operations on their own.
    """

    def __init__(self, user_name: str) -> None:
        super().__init__("create_account", "add a new user", ["user_name"])
        self.user_name = user_name

    def execute(self) -> None:
        self.__create_account(self.user_name)

    def __create_account(self, name):
        print("Creating account...")
        if self.__is_account_already_exist(str(name)):
            print("Account Already Exist")
        else:
            account = Account(*generate_keys(str(name)))
            Ledger().add_account(account)
