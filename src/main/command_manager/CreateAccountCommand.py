from command_manager.Command import Command

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
            print("Account Already Exist")
        else:
            account = Account(*generate_keys(str(name)))
            Ledger().add_account(account)

    def __is_account_already_exist(self, name):
        accounts = Ledger()._accounts.values()
        for account in accounts:
            if account.public_key.owner == name:
                return True
            return False
