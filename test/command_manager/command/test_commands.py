import unittest
from unittest.mock import patch, MagicMock, ANY, mock_open, call
from main.command_manager.commands.HelpCommand import HelpCommand
from main.command_manager.commands.AddBlockCommand import AddBlockCommand
from main.command_manager.commands.CreateAccountCommand import CreateAccountCommand
from main.command_manager.commands.ShowAccountCommand import ShowAccountCommand
from main.command_manager.commands.ShowAllAccountsCommand import ShowAllAccountsCommand
from main.command_manager.commands.ShowBlocksCommand import ShowBlocksCommand
from main.command_manager.commands.ShowLedgerCommand import ShowLedgerCommand
from main.ledger.Ledger import Ledger
import re

from main.ledger.account.Account import Account
from main.utils.fake_crypto import PublicKey, PrivateKey


# These tests will simulate the execution of the commands to verify their correct behavior.

class TestAddBlockCommand(unittest.TestCase):
    def setUp(self):
        self.block_type = "OpenNanocoin"
        self.previous_hash = "HSDJSK52S4W5DADW4W7S5DQ55A"
        self.args = ["100", "PWOEPWOS125D4SD8W5S6DS3DS"]
        self.command = AddBlockCommand(self.block_type, self.previous_hash, self.args)

    @patch('main.ledger.Ledger.Ledger.get_block')
    def test_previous_block_not_found(self, mock_get_block):
        mock_get_block.side_effect = Exception("Block not found")
        with patch('sys.stdout', new=MagicMock()) as fake_out:
            self.command.execute()
            fake_out.write.assert_any_call(f"Previous block {self.previous_hash} not found. ")
            fake_out.write.assert_any_call("\n")

    @patch('main.ledger.Ledger.Ledger.get_block', return_value=MagicMock(account_public_key="key123"))
    @patch('main.ledger.Ledger.Ledger.get_account')
    def test_account_not_found(self, mock_get_account, mock_get_block):
        mock_get_account.side_effect = Exception("Account not found")
        with patch('sys.stdout', new=MagicMock()) as fake_out:
            self.command.execute()
            fake_out.write.assert_any_call(f"Account {mock_get_block.return_value.account_public_key} not found. ")
            fake_out.write.assert_any_call("\n")


    @patch('main.ledger.Ledger.Ledger.get_block', return_value=MagicMock(account_public_key="key123"))
    @patch('main.ledger.Ledger.Ledger.get_account', return_value=MagicMock())
    @patch('main.dsl.BlockTypeRegister.BlockTypeRegister.__getitem__')
    def test_block_type_not_found(self, mock_block_type, mock_get_account, mock_get_block):
        mock_block_type.side_effect = Exception("Block type not found")
        with patch('sys.stdout', new=MagicMock()) as fake_out:
            self.command.execute()
            fake_out.write.assert_any_call(f"Block type {self.block_type} not found. ")
            fake_out.write.assert_any_call("\n")


class TestCreateAccountCommand(unittest.TestCase):

    def setUp(self):
        self.command = CreateAccountCommand("Alice")

    @patch('main.ledger.Ledger.Ledger.add_account')
    @patch('main.utils.fake_crypto.generate_keys', return_value=('public_key', 'private_key'))
    @patch.object(Ledger, 'accounts', new_callable=lambda: {'123': MagicMock(public_key=MagicMock(owner='Alice'))})
    def test_create_account_already_exists(self, mock_accounts, mock_generate_keys, mock_add_account):
        # Simulate that an account with the same name already exists
        with patch('sys.stdout', new=MagicMock()) as fake_out:
            self.command.execute()
            fake_out.write.assert_any_call("Account already exists. Please choose another name.")
            mock_add_account.assert_not_called()

    @patch('main.ledger.Ledger.Ledger.add_account')
    @patch('main.utils.fake_crypto.generate_keys')
    @patch.object(Ledger, 'accounts', new_callable=lambda: {})
    def test_create_account_success(self, mock_accounts, mock_generate_keys, mock_add_account):
        public_key = PublicKey('Alice')
        private_key = PrivateKey('Alice')
        mock_generate_keys.return_value = (private_key, public_key)

        with patch('sys.stdout', new=MagicMock()) as fake_out:
            self.command.execute()
            args, kwargs = mock_add_account.call_args
            created_account = args[0]  # This should be the Account instance passed to add_account

            self.assertIsInstance(created_account, Account)
            self.assertEqual(created_account.public_key.key, public_key.key)

            # We use ANY to assert the method was called with any instance of Account
            mock_add_account.assert_called_once_with(ANY)
            fake_out.write.assert_not_called()


class TestHelpCommand(unittest.TestCase):
    def setUp(self):
        self.command = HelpCommand()

    @patch('builtins.print')
    @patch('builtins.open', new_callable=mock_open)
    def test_execute(self, mock_file_open, mock_print):
        self.command.execute()

        # Check that print was called correctly
        mock_print.assert_any_call(self.command)
        mock_print.assert_called_with("Help information has been written to commands_help.txt\n")

        # Check that the file was written to correctly
        mock_file_open.assert_called_once_with("commands_help.txt", "w")
        mock_file_open().write.assert_called_once_with(str(self.command))


class TestShowAccountCommand(unittest.TestCase):
    @patch('main.ledger.Ledger.Ledger.get_account')
    def test_execute_account_found(self, mock_get_account):
        account = MagicMock()
        mock_get_account.return_value = account
        command = ShowAccountCommand("pub_key_DAFDJFABNSAKPER5D589F6DFD")
        with patch('sys.stdout', new=MagicMock()) as fake_out:
            command.execute()
            fake_out.write.assert_any_call(str(account))

    @patch('main.ledger.Ledger.Ledger.get_account', side_effect=Exception("Account not found."))
    def test_execute_account_not_found(self, mock_get_account):
        command = ShowAccountCommand("pub_key_DAFDJFABNSAKPER5D589F6DFD")
        with patch('sys.stdout', new=MagicMock()) as fake_out:
            command.execute()
            fake_out.write.assert_any_call("Account not found.")

class TestShowAllAccountsCommand(unittest.TestCase):
    def setUp(self):
        self.command = ShowAllAccountsCommand()

    @patch('builtins.print')
    @patch.object(Ledger, 'accounts', new_callable=lambda: {
         'Alice': Account(PrivateKey('Alice'), PublicKey('Alice')),
         'Bob': Account(PrivateKey('Bob'), PublicKey('Bob'))
    })
    def test_execute(self, mock_accounts, mock_print):
        # Setup mock accounts with real or consistent mock keys
        alice_key = PublicKey('Alice')
        bob_key = PublicKey('Bob')
        self.command.execute()

        expected_output = (
                'Ledger contains the following accounts: \n' +
                f'- Alice - {alice_key.key}\n' +
                f'- Bob - {bob_key.key}\n'
        )
        mock_print.assert_called_once_with(expected_output)

    @patch('builtins.print')
    @patch.object(Ledger, 'accounts', new_callable=lambda: {})
    def test_execute_no_accounts(self, mock_accounts, mock_print):
        self.command.execute()
        # The expected output when there are no accounts in the ledger
        expected_output = 'Ledger contains the following accounts: \n'

        # Check if print was called with the correct message
        mock_print.assert_called_once_with(expected_output)


# class TestShowBlocksCommand(unittest.TestCase):
#     def setUp(self):
#         self.command = ShowBlocksCommand()
#
#     @patch('builtins.print')
#     @patch('main.dsl.BlockTypeRegister.BlockTypeRegister.__str__', return_value="Registered Block Types")
#     def test_execute(self, mock_block_type_register_str, mock_print):
#         # Execute the command
#         self.command.execute()
#
#         # Check if print was called correctly with the expected string from BlockTypeRegister
#         mock_print.assert_called_once_with("Registered Block Types")


class TestShowLedgerCommand(unittest.TestCase):
    def setUp(self):
        # Reset Ledger's instance before each test
        Ledger._instances = {}

    @patch('builtins.print')
    def test_execute(self, mock_print):
        # Creating a mock for the Ledger.__str__ method
        with patch.object(Ledger, '__str__', return_value="Current Ledger State") as mock_ledger_str:
            command = ShowLedgerCommand()
            command.execute()

            # Assert that print was called with the correct string from Ledger.__str__()
            mock_print.assert_called_once_with("Current Ledger State")

    def tearDown(self):
        # Clean up Ledger's instance after each test
        Ledger._instances = {}


