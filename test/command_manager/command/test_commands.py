import unittest
from unittest.mock import patch, MagicMock, call

from main.command_manager.commands.AddBlockCommand import AddBlockCommand



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




if __name__ == '__main__':
    unittest.main()
