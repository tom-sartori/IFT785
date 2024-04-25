import unittest

unittest.TestLoader.sortTestMethodsUsing = None

import os
from main.dsl.Action import (
    receive,
    assign_balance_when_opening,
    decrease_balance,
    increase_balance,
    send,
    _transaction_amount_fee,
    _is_divisible)
from main.dsl.BlockTypeRegister import BlockTypeRegister
from main.dsl.Dsl import Dsl
from main.dsl.Verification import account_exists, is_block_unique_in_chain
from main.ledger.Ledger import Ledger
from main.ledger.account.Account import Account
from main.utils.fake_crypto import generate_keys


class TestActions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.current_directory = os.getcwd()
        cls.dsl = Dsl(dsl_file_name=cls.current_directory + '/resources/dsl.json')
        BlockTypeRegister().add_block_types(cls.dsl.blocks)
        cls.genesis_account = Account(*generate_keys('Genesis'))
        Ledger().add_account(cls.genesis_account)
        cls.second_account = Account(*generate_keys('Second'))
        Ledger().add_account(cls.second_account)

        # Open Nanocoin for Genesis.
        cls.genesis_open_nanocoin = BlockTypeRegister()['OpenNanocoin'](cls.genesis_account.head)
        cls.genesis_account.add_block(cls.genesis_open_nanocoin)

        # Open Nanocoin for Second.
        cls.second_account.add_block(BlockTypeRegister()['OpenNanocoin'](cls.second_account.head))

        # Send 50 Nanocoins from Genesis to Second.
        cls.send_block = BlockTypeRegister()['Send'](
            previous_block=cls.genesis_account.head,
            receiver=cls.second_account.public_key.key,
            amount=40,
            open_hash=cls.genesis_open_nanocoin.hash
        )
        cls.genesis_account.add_block(cls.send_block)

        # Receive Nanocoins from Genesis to Second.
        cls.receive_block = BlockTypeRegister()['Receive'](previous_block=cls.second_account.head,
                                                           send_hash=cls.send_block.hash)
        cls.second_account.add_block(cls.receive_block)

    def test_assign_balance_when_opening(self):
        test_account = Account(*generate_keys('Test Account'))
        Ledger().add_account(test_account)
        test_open_nanocoin = BlockTypeRegister()['OpenNanocoin'](test_account.head)
        assign_balance_when_opening(test_open_nanocoin, account=None)
        self.assertEqual(test_open_nanocoin.data['balance'], 100)

    def test_send(self):
        block = self.genesis_account.head
        current_balance = block.data['balance']
        send(block, 10, self.genesis_account.head.hash)
        self.assertEqual(current_balance, block.data['balance'] + 10)

    def test_receive(self):
        new_send_block = BlockTypeRegister()['Send'](
            previous_block=self.genesis_account.head,
            receiver=self.second_account.public_key.key,
            amount=5,
            open_hash=self.genesis_account.head.hash
        )
        self.genesis_account.add_block(new_send_block)
        block = self.second_account.head
        current_balance = block.data['balance']
        receive(block, new_send_block.hash)
        self.assertEqual(block.data['balance'], current_balance + 5)

    def test_account_exists(self):
        self.assertTrue(account_exists(self.genesis_account.public_key.key))

    def test_decrease_balance(self):
        block = self.genesis_account.head
        block.data['balance'] = 100
        amount = 20
        amount_fee = 5
        decrease_balance(block, amount, amount_fee)
        self.assertEqual(block.data['balance'], 100 - 20 - 5)

    def test_increase_balance(self):
        block = self.genesis_account.head
        block.data['balance'] = 100
        amount = 20
        increase_balance(block, amount)
        self.assertEqual(block.data['balance'], 100 + 20)

    def test_is_divisible(self):
        block = self.genesis_account.head
        self.assertTrue(_is_divisible(open_hash=self.genesis_account.head.hash))

    def test_transaction_amount_fee(self):
        self.assertEqual(_transaction_amount_fee(transaction_fee=0.05, amount=40), 2)

    # def test_send_block_with_fee(self):
    #     self.assertEqual(send_with_fee(block=self.genesis_account.head, amount=40, open_hash=self.genesis_open_nanocoin.hash), 25)

    def test_is_block_unique_in_chain(self):
        self.assertTrue(is_block_unique_in_chain(block=self.genesis_account.head))

    def test_cannot_open_nanocoin(self):
        with self.assertRaises(Exception):
            new_genesis_open_nanocoin = BlockTypeRegister()['OpenNanocoin'](self.genesis_account.head)
            another_open_nanocoin = BlockTypeRegister()['OpenNanocoin'](self.genesis_account.head)
            self.genesis_account.add_block(new_genesis_open_nanocoin)
            self.genesis_account.add_block(another_open_nanocoin)
