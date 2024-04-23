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
# genesis_account: Account = Account(*generate_keys('Genesis'))
# Ledger().add_account(genesis_account)
# second_account: Account = Account(*generate_keys('Second'))
# Ledger().add_account(second_account)
 
 
# # Open Nanocoin for Genesis.
# genesis_open_nanocoin = BlockTypeRegister()['OpenNanocoin'](genesis_account.head)
# genesis_account.add_block(genesis_open_nanocoin)
 
# # Open Nanocoin for Second.
# second_account.add_block(BlockTypeRegister()['OpenNanocoin'](second_account.head))
 
# # Send 50 Nanocoins from Genesis to Second.
 
# send_block = BlockTypeRegister()['Send'](
#     previous_block=genesis_account.head,
#     receiver=second_account.public_key.key,
#     amount=40,
#     open_hash=genesis_open_nanocoin.hash
# )
# # print("******************************************")
# genesis_account.add_block(send_block)
 
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
#     block = genesis_account.head
#     set_balance(block,send_block.hash)
#     assert block.data['balance'] == 100-40
   
 
# def test_set_data_from_other_block_hash():
#     block = genesis_account.head
#     set_data_from_other_block_hash(block,receive_block.hash,"balance")
#     assert block.data['balance'] == 140
 
 
# def test_send():
#     block = genesis_account.head
#     current_balance = block.data['balance']
#     send(block,10,genesis_open_nanocoin.hash)
#     assert current_balance  == block.data['balance'] + 10
 
# def test_receive():
#     new_send_block = BlockTypeRegister()['Send'](
#     previous_block=genesis_account.head,
#     receiver=second_account.public_key.key,
#     amount=5,
#     open_hash=genesis_open_nanocoin.hash
#     )
#     genesis_account.add_block(new_send_block)
#     block = second_account.head
#     current_balance = block.data['balance']
#     receive(block,new_send_block.hash)
#     assert block.data['balance'] == current_balance + 5
   
   
# def test_account_exists():
#     assert account_exists(genesis_account.public_key.key)

# def test_decreaseBalance():
#     # initialise_test()
#     block = genesis_account.head
#     block.data['balance']=100
#     amount=20
#     amount_fee=5

#     decrease_balance(block,amount,amount_fee)
#     assert block.data['balance'] == 100 - 20 - 5

# def test_increaseBalance():
#     block = genesis_account.head
#     block.data['balance']=100
#     amount = 20
#     increase_balance(block,amount)
#     assert block.data['balance'] == 100 + 20
   
# def test_isDivisible():
#     block = genesis_account.head
#     # block.data['isDivisible']=100
#     assert _is_divisible(open_hash  =genesis_open_nanocoin.hash)
 
# # def test_send_can_interact_with():
# #     assert can_interact_with(block=send_block, open_hash=genesis_open_nanocoin.hash)
 
# # def test_receive_can_interact_with():
# #     assert can_interact_with(block=receive_block, open_hash=genesis_open_nanocoin.hash)
 
# # def test_cannot_interact_with():
# #     assert  can_interact_with(block=genesis_account.head, open_hash=genesis_open_nanocoin.hash)
 
 
# def test_transaction_amount_fee():
#     assert _transaction_amount_fee(transaction_fee=(0.05), amount=40) == 2
    
# # def test_send_with_fee():
# #     pass
# #     send_with_fee(block=genesis_account.head, amount=40, open_hash=genesis_open_nanocoin.hash)

# def test_send_block_with_fee():
#     send_with_fee(block=genesis_account.head, amount=40, open_hash=genesis_open_nanocoin.hash) ==25
    
# def test_is_block_unique_in_chain():
#     assert is_block_unique_in_chain(block=genesis_open_nanocoin)
    

# def test_cannot_open_nanocoin():
#     with pytest.raises(Exception):
#         new_genesis_open_nanocoin = BlockTypeRegister()['OpenNanocoin'](genesis_account.head)
#         new_genesis_account.add_block(genesis_open_nanocoin)


import unittest
unittest.TestLoader.sortTestMethodsUsing = None

import os
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
        cls.receive_block = BlockTypeRegister()['Receive'](previous_block=cls.second_account.head, send_hash=cls.send_block.hash)
        cls.second_account.add_block(cls.receive_block)

    # def test_set_balance(self):
    #     block = self.genesis_account.head
    #     print("First account is ", self.genesis_account)
    #     print("testing set balance",block.data)
    #     set_balance(block, self.send_block.hash)
    #     self.assertEqual(block.data['balance'], 100 - 40)

    def test_assign_balance_when_opening(self):
        test_account = Account(*generate_keys('Test Account'))
        Ledger().add_account(test_account)
        test_open_nanocoin = BlockTypeRegister()['OpenNanocoin'](test_account.head)
        assign_balance_when_opening(test_open_nanocoin, account=None)
        self.assertEqual(test_open_nanocoin.data['balance'], 100)

  

    # def test_set_data_from_other_block_hash(self):
    #     block = self.genesis_account.head
    #     set_data_from_other_block_hash(block, self.second_account.head.hash, "balance")
    #     self.assertEqual(block.data['balance'], 140)

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
    
# if __name__ == '__main__':
#     loader = CustomTestLoader()
#     suite = loader.loadTestsFromTestCase(TestSequence)
#     runner = unittest.TextTestRunner()
#     runner.run(suite)

# import unittest

# class TestSequence(unittest.TestCase):
#     def test_assign_balance_when_opening(self):
#         # Your test code here
#         pass

#     def test_another_test_function(self):
#         # Another test function
#         pass

# if __name__ == '__main__':
#     loader = unittest.TestLoader()
#     tests = loader.loadTestsFromTestCase(TestActions)
#     suite = unittest.TestSuite(tests)
#     unittest.TextTestRunner(verbosity=2).run(suite)