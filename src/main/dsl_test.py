import pytest
import os 

from dsl.BlockTypeRegister import BlockTypeRegister
from dsl.Dsl import Dsl
from ledger.Ledger import Ledger
from ledger.account.Account import Account
from utils.fake_crypto import generate_keys, Signature
from ledger.block.Block import Block
# from resources.documentation import documentation
# from resources.dsl import dsl

from ledger.block.Block import Block
from ledger.block.GenesisBlock import GenesisBlock

from dsl.Action import  (
 receive, 
 assign_balance_when_opening ,
 set_balance ,
 decrease_balance,
 increase_balance ,
 set_data_from_other_block_hash,
 send ,
 transaction_amount_fee,
 receive,
 is_divisible)

from dsl.Verification import (
account_exists,
is_balance_valid,
open_block_does_not_exist,
can_interact_with,
is_divisible )

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# def initialise_test():
current_directory = os.getcwd()
dsl: Dsl = Dsl(dsl_file_name=current_directory + '/resources/dsl.json')
BlockTypeRegister().add_block_types(dsl.blocks)
print(BlockTypeRegister())
print("******************************************")
# Create two accounts.
private_key_one, public_key_one = generate_keys('Genesis')
print()
genesis_account: Account = Account(private_key_one,public_key_one)
Ledger().add_account(genesis_account)
second_account: Account = Account(*generate_keys('Second'))
Ledger().add_account(second_account)

# Open Nanocoin for Genesis.
genesis_open_nanocoin = BlockTypeRegister()['OpenNanocoin'](genesis_account.head)
genesis_account.add_block(genesis_open_nanocoin)

# Open Nanocoin for Second.
second_account.add_block(BlockTypeRegister()['OpenNanocoin'](second_account.head))

# Send 50 Nanocoins from Genesis to Second.

send_block = BlockTypeRegister()['Send'](
    previous_block=genesis_account.head,
    receiver=second_account.public_key.key,
    amount=40,
    open_hash=genesis_open_nanocoin.hash
)
# print("******************************************")
# genesis_account.add_block(send_block)

# Receive Nanocoins from Genesis to Second.
receive_block = BlockTypeRegister()['Receive'](previous_block=second_account.head, send_hash=send_block.hash)
# second_account.add_block(receive_block)

# @pytest.mark.test
def test_decreaseBalance():
    # initialise_test()
    block = genesis_account.head 
    block.data['balance']=100
    amount=20
    amount_fee=5
    
    decrease_balance(block,amount,amount_fee)
    
    assert block.data['balance'] == 100 - 20 - 5
    
def test_increaseBalance():
    block = genesis_account.head
    block.data['balance']=100
    amount = 20
    increase_balance(block,amount)
    assert block.data['balance'] == 100 + 20
    
def test_isDivisible():
    block = genesis_account.head
    # block.data['isDivisible']=100
    assert is_divisible(open_hash  =genesis_open_nanocoin.hash)

def test_send_can_interact_with():
    assert can_interact_with(block=send_block, open_hash=genesis_open_nanocoin.hash)

def test_receive_can_interact_with():
    assert can_interact_with(block=receive_block, open_hash=genesis_open_nanocoin.hash)

def test_cannot_interact_with():
    assert not can_interact_with(block=genesis_account.head, open_hash=genesis_open_nanocoin.hash)


def test_transaction_amount_fee():
    assert transaction_amount_fee(transaction_fee=(0.05), amount=40, open_hash=genesis_open_nanocoin.hash) == 2


def test_open_block_does_not_exist():
    assert not open_block_does_not_exist(block=genesis_open_nanocoin)

def test_open_block_exists():
    # genesis_open_nanocoin_second = BlockTypeRegister()['OpenNanocoin'](genesis_account.head)
    # assert not genesis_account.add_block(genesis_open_nanocoin_second)
    assert not open_block_does_not_exist(block=genesis_account.head)