import unittest
from utils.fake_crypto import generate_keys
from ledger.account.Account import Account

#À déplacer dans src/test/ledger/account

class Account_test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
       (cls.genesisPrivateKey, cls.genesisPublicKey) = generate_keys('Genesis')


    def setUp(self):
        self.account = Account(self.genesisPrivateKey, self.genesisPublicKey)


    def tearDown(self):
        self.account = None

    @classmethod
    def tearDownClass(cls):
        cls.genesisPrivateKey = None
        cls.genesisPublicKey = None


    def test_publicKey(self):
        self.assertEqual(self.account.public_key, self.genesisPublicKey)





if __name__ == '__main__':
    unittest.main()
