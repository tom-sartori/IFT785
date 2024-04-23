# import os
# import sys
# import pytest
# from main.dsl.Action import (
#     receive,
#     assign_balance_when_opening,
#     set_balance,
#     decrease_balance,
#     increase_balance,
#     set_data_from_other_block_hash,
#     send,
#     send_with_fee,
#     _transaction_amount_fee,
#     _is_divisible)
# from main.dsl.BlockTypeRegister import BlockTypeRegister
# from main.dsl.Dsl import Dsl
# from main.dsl.Verification import (
#     account_exists,
#     # open_block_exists,
#     # can_interact_with,
#     is_block_unique_in_chain,
    
#     )
# from main.ledger.Ledger import Ledger
# from main.ledger.account.Account import Account
# from main.utils.fake_crypto import generate_keys

# current_directory = os.getcwd()
# dsl: Dsl = Dsl(dsl_file_name=current_directory + '/resources/dsl.json')
# BlockTypeRegister().add_block_types(dsl.blocks)
# print(BlockTypeRegister())
# print("******************************************")
# # Create two accounts.
# first_account: Account = Account(*generate_keys('Genesis'))
# Ledger().add_account(first_account)
# second_account: Account = Account(*generate_keys('Second'))
# Ledger().add_account(second_account)
 
 
# # Open Nanocoin for Genesis.
# genesis_open_nanocoin = BlockTypeRegister()['OpenNanocoin'](first_account.head)
# first_account.add_block(genesis_open_nanocoin)
 
# # Open Nanocoin for Second.
# second_account.add_block(BlockTypeRegister()['OpenNanocoin'](second_account.head))
 
# # Send 50 Nanocoins from Genesis to Second.
 
# send_block = BlockTypeRegister()['Send'](
#     previous_block=first_account.head,
#     receiver=second_account.public_key.key,
#     amount=40,
#     open_hash=genesis_open_nanocoin.hash
# )
# # print("******************************************")
# first_account.add_block(send_block)
 
# # Receive Nanocoins from Genesis to Second.
# receive_block = BlockTypeRegister()['Receive'](previous_block=second_account.head, send_hash=send_block.hash)
# second_account.add_block(receive_block)
 
# # def test_open_block_does_not_exist():
# #     test_account: Account = Account(*generate_keys('Test Account'))
# #     Ledger().add_account(test_account)
# #     test_open_nanocoin = BlockTypeRegister()['OpenNanocoin'](test_account.head)
# #     assert  open_block_does_not_exist(block=test_open_nanocoin)
 
 
# # def test_open_block_exists():
# #     assert not open_block_does_not_exist(block=genesis_open_nanocoin)
 
 
 
# def test_assign_balance_when_opening():
#     test_account: Account = Account(*generate_keys('Test Account'))
#     Ledger().add_account(test_account)
#     test_open_nanocoin = BlockTypeRegister()['OpenNanocoin'](test_account.head)
#     block = test_open_nanocoin
#     assign_balance_when_opening(block,account=None)
#     print(block)
#     assert block.data['balance'] == 100
 
# def test_set_balance():
#     block = first_account.head
#     set_balance(block,send_block.hash)
#     assert block.data['balance'] == 100-40
   
 
# def test_set_data_from_other_block_hash():
#     block = first_account.head
#     set_data_from_other_block_hash(block,receive_block.hash,"balance")
#     assert block.data['balance'] == 140
 
 
# def test_send():
#     block = first_account.head
#     current_balance = block.data['balance']
#     send(block,10,genesis_open_nanocoin.hash)
#     assert current_balance  == block.data['balance'] + 10
 
# def test_receive():
#     new_send_block = BlockTypeRegister()['Send'](
#     previous_block=first_account.head,
#     receiver=second_account.public_key.key,
#     amount=5,
#     open_hash=genesis_open_nanocoin.hash
#     )
#     first_account.add_block(new_send_block)
#     block = second_account.head
#     current_balance = block.data['balance']
#     receive(block,new_send_block.hash)
#     assert block.data['balance'] == current_balance + 5
   
   
# def test_account_exists():
#     assert account_exists(first_account.public_key.key)

# def test_decreaseBalance():
#     # initialise_test()
#     block = first_account.head
#     block.data['balance']=100
#     amount=20
#     amount_fee=5

#     decrease_balance(block,amount,amount_fee)
#     assert block.data['balance'] == 100 - 20 - 5

# def test_increaseBalance():
#     block = first_account.head
#     block.data['balance']=100
#     amount = 20
#     increase_balance(block,amount)
#     assert block.data['balance'] == 100 + 20
   
# def test_isDivisible():
#     block = first_account.head
#     # block.data['isDivisible']=100
#     assert _is_divisible(open_hash  =genesis_open_nanocoin.hash)
 
# # def test_send_can_interact_with():
# #     assert can_interact_with(block=send_block, open_hash=genesis_open_nanocoin.hash)
 
# # def test_receive_can_interact_with():
# #     assert can_interact_with(block=receive_block, open_hash=genesis_open_nanocoin.hash)
 
# # def test_cannot_interact_with():
# #     assert  can_interact_with(block=first_account.head, open_hash=genesis_open_nanocoin.hash)
 
 
# def test_transaction_amount_fee():
#     assert _transaction_amount_fee(transaction_fee=(0.05), amount=40) == 2
    
# # def test_send_with_fee():
# #     pass
# #     send_with_fee(block=first_account.head, amount=40, open_hash=genesis_open_nanocoin.hash)

# def test_send_block_with_fee():
#     send_with_fee(block=first_account.head, amount=40, open_hash=genesis_open_nanocoin.hash) ==25
    
# def test_is_block_unique_in_chain():
#     assert is_block_unique_in_chain(block=genesis_open_nanocoin)
    

# def test_cannot_open_nanocoin():
#     with pytest.raises(Exception):
#         new_genesis_open_nanocoin = BlockTypeRegister()['OpenNanocoin'](first_account.head)
#         new_genesis_account.add_block(genesis_open_nanocoin)
        
        

# '''     
# python -m unittest discover <test_directory>
# # or
# python -m unittest discover -s <directory> -p '*_test.py'

# python -m pytest -v --ignore= <directory>

# '''


import unittest
import os
import sys
from main.dsl.Action import (
    receive,
    assign_balance_when_opening,
    set_balance,
    decrease_balance,
    increase_balance,
    set_data_from_other_block_hash,
    send,
    send_with_fee,
    _transaction_amount_fee,
    _is_divisible)
from main.dsl.BlockTypeRegister import BlockTypeRegister
from main.dsl.Dsl import Dsl
from main.dsl.Verification import (
    account_exists,
    is_block_unique_in_chain,
)
from main.ledger.Ledger import Ledger
from main.ledger.account.Account import Account
from main.utils.fake_crypto import generate_keys

class TestDsl(unittest.TestCase):
    def setUp(self):
        self.current_directory = os.getcwd()
        self.dsl: Dsl = Dsl(dsl_file_name=self.current_directory + '/resources/dsl.json')
        BlockTypeRegister().add_block_types(self.dsl.blocks)
        self.first_account: Account = Account(*generate_keys('First'))
        Ledger().add_account(self.first_account)
        self.second_account: Account = Account(*generate_keys('Second'))
        Ledger().add_account(self.second_account)
        self.genesis_open_nanocoin = BlockTypeRegister()['OpenNanocoin'](self.first_account.head)
        self.first_account.add_block(self.genesis_open_nanocoin)
        self.second_account.add_block(BlockTypeRegister()['OpenNanocoin'](self.second_account.head))
        self.send_block = BlockTypeRegister()['Send'](
            previous_block=self.first_account.head,
            receiver=self.second_account.public_key.key,
            amount=40,
            open_hash=self.genesis_open_nanocoin.hash
        )
        self.first_account.add_block(self.send_block)
        self.receive_block = BlockTypeRegister()['Receive'](previous_block=self.second_account.head, send_hash=self.send_block.hash)
        self.second_account.add_block(self.receive_block)

    def test_assign_balance_when_opening(self):
        test_account: Account = Account(*generate_keys('Test Account'))
        Ledger().add_account(test_account)
        test_open_nanocoin = BlockTypeRegister()['OpenNanocoin'](test_account.head)
        block = test_open_nanocoin
        assign_balance_when_opening(block, account=None)
        self.assertEqual(block.data['balance'], 100)

    def test_set_balance(self):
        block = self.first_account.head
        set_balance(block, self.send_block.hash)
        self.assertEqual(block.data['balance'], 100 - 40)

    def test_set_data_from_other_block_hash(self):
        block = self.first_account.head
        set_data_from_other_block_hash(block, self.receive_block.hash, "balance")
        self.assertEqual(block.data['balance'], 140)

    def test_send(self):
        block = self.first_account.head
        current_balance = block.data['balance']
        send(block, 10, self.genesis_open_nanocoin.hash)
        self.assertEqual(current_balance, block.data['balance'] + 10)

    def test_receive(self):
        new_send_block = BlockTypeRegister()['Send'](
            previous_block=self.first_account.head,
            receiver=self.second_account.public_key.key,
            amount=5,
            open_hash=self.genesis_open_nanocoin.hash
        )
        self.first_account.add_block(new_send_block)
        block = self.second_account.head
        current_balance = block.data['balance']
        receive(block, new_send_block.hash)
        self.assertEqual(block.data['balance'], current_balance + 5)

    def test_account_exists(self):
        self.assertTrue(account_exists(self.first_account.public_key.key))

    def test_decreaseBalance(self):
        block = self.first_account.head
        block.data['balance'] = 100
        amount = 20
        amount_fee = 5
        decrease_balance(block, amount, amount_fee)
        self.assertEqual(block.data['balance'], 100 - 20 - 5)

    def test_increaseBalance(self):
        block = self.first_account.head
        block.data['balance'] = 100
        amount = 20
        increase_balance(block, amount)
        self.assertEqual(block.data['balance'], 100 + 20)

    def test_isDivisible(self):
        block = self.first_account.head
        self.assertTrue(_is_divisible(open_hash=self.genesis_open_nanocoin.hash))

    def test_transaction_amount_fee(self):
        self.assertEqual(_transaction_amount_fee(transaction_fee=0.05, amount=40), 2)

    def test_send_block_with_fee(self):
        self.assertEqual(send_with_fee(block=self.first_account.head, amount=40, open_hash=self.genesis_open_nanocoin.hash), 25)

    def test_is_block_unique_in_chain(self):
        self.assertTrue(is_block_unique_in_chain(block=self.genesis_open_nanocoin))

    def test_cannot_open_nanocoin(self):
        with self.assertRaises(Exception):
            new_genesis_open_nanocoin = BlockTypeRegister()['OpenNanocoin'](self.first_account.head)
            new_genesis_account = Account(*generate_keys('New Genesis'))
            new_genesis_account.add_block(self.genesis_open_nanocoin)

if __name__ == '__main__':
    unittest.main()