import unittest

from main.ledger.account.Account import Account
from main.utils.fake_crypto import generate_keys
from main.ledger.block.Block import Block
from main.ledger.Ledger import Ledger
from main.utils.fake_crypto import generate_keys


class TestAccount(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        (cls.genesisPrivateKey, cls.genesisPublicKey) = generate_keys('Account_test')

        cls.other_account: Account = Account(*generate_keys('Account_test2'))

    def setUp(self):
        self.account = Account(self.genesisPrivateKey, self.genesisPublicKey)
        self.block = Block(self.account.head)

    def tearDown(self):
        self.account = None
        self.block = None
        Ledger()._blocks.clear() #Clear the ledger to be able to replace the account

    @classmethod
    def tearDownClass(cls):
        cls.genesisPrivateKey = None
        cls.genesisPublicKey = None

    #------- TEST -------
    #-------Test getter-------
    def test_publicKey(self):
        self.assertEqual(self.account.public_key, self.genesisPublicKey)

    #-------Test the balance in the account-------
    def test_getBalances_NoBalance(self):
        self.assertEqual(self.account.balances, {})

    def test_getBalances_OneBalance_OneBlock(self):
        self.block.add_data('balance', 100)
        self.block.add_data('unit', 'coin')
        self.block.sign(self.genesisPrivateKey)

        self.account.add_block(self.block)

        self.assertEqual(self.account.balances, {'coin': 100})

    #TODO : Correct the test
    #def test_getBalances_UseOpenHash(self):
    #   anotherBlock = Block(self.account.head)
    #   anotherBlock.add_data('balance', 100)
    #   anotherBlock.add_data('open_hash', 'coin')
    #   anotherBlock.sign(self.genesisPrivateKey)
    #   self.account.add_block(anotherBlock)
    #
    #   self.assertEqual(self.account.balances, {'coin': 100})

    def test_getBalances_OneBalance_MultipleBlock(self):
        self.block.add_data('balance', 100)
        self.block.add_data('unit', 'coin')
        self.block.sign(self.genesisPrivateKey)
        self.account.add_block(self.block)

        thirdBlock = Block(self.account.head)
        thirdBlock.add_data('balance', 200)
        thirdBlock.add_data('unit', 'coin')
        thirdBlock.sign(self.genesisPrivateKey)
        self.account.add_block(thirdBlock)

        self.assertEqual(self.account.balances, {'coin': 200})

    def test_getBalances_MultipleBalance(self):
        self.block.add_data('balance', 100)
        self.block.add_data('unit', 'coin')
        self.block.sign(self.genesisPrivateKey)
        self.account.add_block(self.block)

        thirdBlock = Block(self.account.head)
        thirdBlock.add_data('balance', 200)
        thirdBlock.add_data('unit', 'coin2')
        thirdBlock.sign(self.genesisPrivateKey)
        self.account.add_block(thirdBlock)

        self.assertEqual(self.account.balances, {'coin': 100, 'coin2': 200})

    def test_getBalance(self):
        self.block.add_data('balance', 100)
        self.block.add_data('unit', 'coin')
        self.block.sign(self.genesisPrivateKey)
        self.account.add_block(self.block)

        self.assertEqual(self.account.get_balance('coin'), 100)

    def test_getBalanceException_NoUnit(self):
        with self.assertRaises(Exception):
            self.account.get_balance('UnitDontExist')

    #-------Test adding block to the account-------
    def test_addBlock(self):
        self.account.add_block(self.block)
        self.assertEqual(self.account.head, self.block)

    def test_addBlock_BlockAlreadySigned(self):
        self.block.sign(self.genesisPrivateKey)

        self.account.add_block(self.block)

        self.assertEqual(self.account.head, self.block)

    def test_addBlockException_BlockBySomeoneElse(self):
        otherBlock = Block(self.other_account.head)

        with self.assertRaises(Exception):
            self.account.add_block(otherBlock)

    def test_addBlockException_BlockSignedbySomeoneElse(self):
        otherBlock = Block(self.other_account.head)
        otherBlock.sign(self.other_account._private_key)

        with self.assertRaises(Exception):
            self.account.add_block(otherBlock)

    #-------Test integrity of account-------
    def test_Verify(self):
        self.assertTrue(self.account.verify())

        self.account.add_block(self.block)
        self.assertTrue(self.account.verify())

    def test_VerifyException_LatestBlockNotVerify(self):
        self.account._chain._block_list.append(self.block)
        self.assertFalse(self.account.verify())

    def test_Verification_BlockNotVerify(self):
        self.account._chain._block_list.append(self.block)

        thirdBlock = Block(self.account.head)
        self.account._chain._block_list.append(thirdBlock)
        self.assertFalse(self.account.verify())

    def test_VerifyException_PreviousBlockNotGood(self):
        self.account._chain._block_list.append(self.account.head)
        self.assertFalse(self.account.verify())
