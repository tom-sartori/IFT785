import os
import pytest

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.main.dsl.BlockTypeRegister import BlockTypeRegister
from src.main.dsl.Dsl import Dsl
from src.main.ledger.Ledger import Ledger
from src.main.ledger.account.Account import Account
from src.main.utils.fake_crypto import generate_keys

# from resources.documentation import documentation
# from resources.dsl import dsl

from src.main.ledger.block.Block import Block
from src.main.ledger.block.GenesisBlock import GenesisBlock

from src.main.dsl.Action import  (
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

from src.main.dsl.Verification import (
account_exists,
is_balance_valid,
open_block_does_not_exist,
can_interact_with,
is_divisible )

current_directory = os.getcwd()
dsl: Dsl = Dsl(dsl_file_name=current_directory + '/resources/dsl.json')
BlockTypeRegister().add_block_types(dsl.blocks)

first_account: Account = Account(*generate_keys('Genesis'))
Ledger().add_account(first_account)
second_account: Account = Account(*generate_keys('Second'))
Ledger().add_account(second_account)

# Open Nanocoin for Genesis.
genesis_open_nanocoin = BlockTypeRegister()['OpenNanocoin'](first_account.head)
first_account.add_block(genesis_open_nanocoin)

# # Open Nanocoin for Second.
second_account.add_block(BlockTypeRegister()['OpenNanocoin'](second_account.head))

# Send 50 Nanocoins from Genesis to Second.
# send_block = BlockTypeRegister()['Send'](
#     previous_block=first_account.head,
#     receiver=second_account.public_key.key,
#     amount=40,
#     open_hash=genesis_open_nanocoin.hash
# )
@pytest.fixture
def block():
    block  = Block(previous_block= genesis_open_nanocoin.key)
    block.sign(private_key=first_account.private_key)
    return block

def tesequality():
   assert 10 == 11
@pytest.fixture
def decrease_balance():
    return decrease_balance()

# @pytest.mark.test
def test_decreaseBalance(block, amount,amount_fee):
    
    block.data['balance']=100
    amount=20
    amount_fee=10
    
    decrease_balance(block,amount,amount_fee)
    
    assert block.data['balance'] == 100 - 20 -10