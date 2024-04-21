import unittest
from ledger.account.Chain import Chain
from ledger.account.Account import Account
from ledger.block.GenesisBlock import GenesisBlock
from ledger.block.Block import Block
from utils.fake_crypto import generate_keys

#À déplacer dans src/test/ledger/account

class Chain_test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        genesis_account: Account = Account(*generate_keys('Genesis'))
        cls.genesisPublicKey = genesis_account.public_key
        cls.genesisPrivateKey = genesis_account._private_key

        cls.genesis_block = GenesisBlock(cls.genesisPublicKey)
        cls.genesis_block.sign(cls.genesisPrivateKey)

        cls.anotherAccount: Account = Account(*generate_keys('AnotherAccount'))


    def setUp(self):
        self.chaine = Chain(self.genesis_block)

        self.firstBlock = Block(self.genesis_block)
        self.firstBlock.sign(self.genesisPrivateKey)


    def tearDown(self):
        self.chaine = None
        self.firstBlock = None


    @classmethod
    def tearDownClass(cls):
        cls.genesis_block = None



    def test_head_OneBlock(self):
        self.assertEqual(self.chaine.head, self.genesis_block)


    def test_head_MultipleBlock(self):
        self.chaine.add_block(self.firstBlock, self.genesisPublicKey)
        self.assertEqual(self.chaine.head, self.firstBlock)


    def test_initialBlockNumber(self):
        self.assertEqual(len(self.chaine), 1)


    def test_AddBlock(self):
        self.chaine.add_block(self.firstBlock, self.genesisPublicKey)
        self.assertEqual(len(self.chaine), 2)
    

    def test_AddBlockException_HeadNotSigned(self):
        #Can only happen during the __init__ phase, with the genesisBlock

        blockNotSigned = GenesisBlock(self.anotherAccount.public_key)
        #Block not signed
        errorChain = Chain(blockNotSigned)

        secondBlock = Block(errorChain.head)
        secondBlock.sign(self.anotherAccount._private_key)

        with self.assertRaises(Exception):
            errorChain.add_block(secondBlock, self.anotherAccount.public_key)
    

    def test_AddBlockException_NotAddToEnd(self):
        otherBlock = Block(self.chaine.head)
        otherBlock.sign(self.genesisPrivateKey)

        self.chaine.add_block(self.firstBlock, self.genesisPublicKey)

        with self.assertRaises(Exception):
            self.chaine.add_block(otherBlock, self.genesisPublicKey)


    def test_AddBlockException_BlockNotSigned(self):
        otherBlock = Block(self.chaine.head)

        with self.assertRaises(Exception):
            self.chaine.add_block(otherBlock, self.genesisPublicKey)


    def test_AddBlockException_BlockSignatureFailed(self):
        anotherBlock = Block(self.chaine.head)
        anotherBlock.sign(self.anotherAccount._private_key)

        with self.assertRaises(Exception):
            self.chaine.add_block(anotherBlock, self.genesisPublicKey)
        

    def test_Verify(self):
        self.assertTrue(self.chaine.verify(self.genesisPublicKey))

        self.chaine.add_block(self.firstBlock, self.genesisPublicKey)
        self.assertTrue(self.chaine.verify(self.genesisPublicKey))


    def test_VerifyException_LatestBlockNotVerify(self):
        secondBlock = Block(self.chaine.head)
        self.chaine._block_list.append(secondBlock)

        self.assertFalse(self.chaine.verify(self.genesisPublicKey))


    def test_Verification_BlockNotVerify(self):
        secondBlock = Block(self.chaine.head)
        self.chaine._block_list.append(secondBlock)

        thirdBlock = Block(self.chaine.head)
        self.chaine._block_list.append(thirdBlock)
        self.assertFalse(self.chaine.verify(self.genesisPublicKey))


    def test_VerifyException_PreviousBlockNotGood(self):
        self.chaine._block_list.append(self.genesis_block)
        self.assertFalse(self.chaine.verify(self.genesisPublicKey))

    
    def test_getBalances_NoBalance(self):
        self.assertEqual(self.chaine.get_balances(), {})


    def test_getBalances_OneBalance_OneBlock(self):
        anotherBlock = Block(self.chaine.head)
        anotherBlock.add_data('balance', 100)
        anotherBlock.add_data('unit', 'coin')
        anotherBlock.sign(self.genesisPrivateKey)
        self.chaine.add_block(anotherBlock, self.genesisPublicKey)

        self.assertEqual(self.chaine.get_balances(), {'coin':100})

    #def test_getBalances_UseOpenHash(self):
    #    #TODO - Have a test to use the open_hash data from a block
    #    pass


    def test_getBalances_OneBalance_MultipleBlock(self):
        anotherBlock = Block(self.chaine.head)
        anotherBlock.add_data('balance', 100)
        anotherBlock.add_data('unit', 'coin')
        anotherBlock.sign(self.genesisPrivateKey)
        self.chaine.add_block(anotherBlock, self.genesisPublicKey)

        thirdBlock = Block(self.chaine.head)
        thirdBlock.add_data('balance', 200)
        thirdBlock.add_data('unit', 'coin')
        thirdBlock.sign(self.genesisPrivateKey)
        self.chaine.add_block(thirdBlock, self.genesisPublicKey)

        self.assertEqual(self.chaine.get_balances(), {'coin':200})


    def test_getBalances_MultipleBalance(self):
        anotherBlock = Block(self.chaine.head)
        anotherBlock.add_data('balance', 100)
        anotherBlock.add_data('unit', 'coin')
        anotherBlock.sign(self.genesisPrivateKey)
        self.chaine.add_block(anotherBlock, self.genesisPublicKey)

        thirdBlock = Block(self.chaine.head)
        thirdBlock.add_data('balance', 200)
        thirdBlock.add_data('unit', 'coin2')
        thirdBlock.sign(self.genesisPrivateKey)
        self.chaine.add_block(thirdBlock, self.genesisPublicKey)

        self.assertEqual(self.chaine.get_balances(), {'coin':100, 'coin2':200})


    def test_getBalance(self):
        anotherBlock = Block(self.chaine.head)
        anotherBlock.add_data('balance', 100)
        anotherBlock.add_data('unit', 'coin')
        anotherBlock.sign(self.genesisPrivateKey)
        self.chaine.add_block(anotherBlock, self.genesisPublicKey)

        self.assertEqual(self.chaine.get_balance('coin'), 100)

    def test_getBalanceException_NoUnit(self):
        with self.assertRaises(Exception):
            self.chaine.get_balance('UnitDontExist')


if __name__ == '__main__':
    unittest.main()
