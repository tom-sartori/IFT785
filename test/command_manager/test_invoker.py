import unittest
from unittest.mock import patch, MagicMock

from main.command_manager.Invoker import Invoker


class TestInvoker(unittest.TestCase):
    # These tests will check the interaction between Invoker and the commands it is supposed to execute.
    @patch('main.command_manager.CommandFactory.CommandFactory.__getitem__')
    def test_execute_known_command(self, mock_getitem):
        mock_command = MagicMock()
        mock_getitem.return_value = mock_command
        invoker = Invoker("create_account Alice")
        invoker.execute()
        mock_command.execute.assert_called_once()

    def test_execute_unknown_command(self):
        invoker = Invoker("unknown_command")
        with patch('sys.stdout', new=MagicMock()) as fake_out:
            invoker.execute()
            fake_out.write.assert_any_call("Unknown command.")
            # we use assert_any_call instead of assert_called_once because the print() method automatically adds a
            # newline character after the message.
