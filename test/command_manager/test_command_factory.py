import unittest
from main.command_manager.commands.HelpCommand import HelpCommand
from main.command_manager.CommandFactory import CommandFactory
from main.command_manager.commands.AddBlockCommand import AddBlockCommand
from main.command_manager.commands.CreateAccountCommand import CreateAccountCommand
from main.command_manager.commands.ShowAccountCommand import ShowAccountCommand
from main.command_manager.commands.ShowAllAccountsCommand import ShowAllAccountsCommand
from main.command_manager.commands.ShowBlocksCommand import ShowBlocksCommand
from main.command_manager.commands.ShowLedgerCommand import ShowLedgerCommand


class TestCommandFactory(unittest.TestCase):
    # These tests check whether the CommandFactory correctly creates command objects based on input.
    def test_create_account_command(self):
        factory = CommandFactory()
        command = factory["create_account Alice"]
        self.assertIsInstance(command, CreateAccountCommand)
        self.assertEqual(command.user_name, "Alice")

    def test_show_blocks_command(self):
        factory = CommandFactory()
        command = factory["show_blocks"]
        self.assertIsInstance(command, ShowBlocksCommand)

    def test_show_ledger_command(self):
        factory = CommandFactory()
        command = factory["show_ledger"]
        self.assertIsInstance(command, ShowLedgerCommand)

    def test_show_account_command(self):
        factory = CommandFactory()
        command = factory["show_account"]
        self.assertIsInstance(command, ShowAccountCommand)

    def test_show_accounts_command(self):
        factory = CommandFactory()
        command = factory["show_accounts"]
        self.assertIsInstance(command, ShowAllAccountsCommand)

    def test_add_block_command_with_args(self):
        factory = CommandFactory()
        command = factory["add_block OpenNanocoin HSDJSK52S4W5DADW4W7S5DQ55A 100 PWOEPWOS125D4SD8W5S6DS3DS"]
        self.assertIsInstance(command, AddBlockCommand)
        self.assertEqual(command.block_type, "OpenNanocoin")
        self.assertEqual(command.previous_hash, "HSDJSK52S4W5DADW4W7S5DQ55A")
        self.assertEqual(command.args, ['100', 'PWOEPWOS125D4SD8W5S6DS3DS'])

    def test_show_help_command(self):
        factory = CommandFactory()
        command = factory["help"]
        self.assertIsInstance(command, HelpCommand)


    def test_unknown_command(self):
        factory = CommandFactory()
        command = factory["unknown"]
        self.assertIsNone(command)


